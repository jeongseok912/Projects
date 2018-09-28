# 수집일 2018.09.02(일)

# 1. 데이터 가져오기
library(mongolite)
conn <- mongo(db = "youtube",
              collection = "channel",
              url = "mongodb://localhost:27017")
mongo_df <- conn$find('{}')
nrow(mongo_df) * (length(mongo_df) + length(mongo_df$AboutTab) + length(mongo_df$HomeTab) + length(mongo_df$AboutTab$Link))

# 2. 전처리
# 2-1. 구독자순 정렬
mongo_df <- mongo_df[c(order(mongo_df$SubscriberNum, decreasing = T)),]

# 2-2. noise 제거
mongo_df <- mongo_df[-which(mongo_df$AboutTab$Loc == '베트남'),]
mongo_df <- mongo_df[-which(mongo_df$ChannelTitle == ''),]
str(mongo_df)

# 2-3. 결측치 확인
colSums(is.na(mongo_df))

# 3.데이터 프레임 생성
# 3-1. 분석용 데이터 프레임 생성
ch_df_num <- data.frame("subs" = mongo_df$SubscriberNum, "playlist" = mongo_df$PlaylistCount, "video" = mongo_df$VideoCount, 
                    # post, comment 수가 매우 작아 분석 대상 변수로서 무의미 하다고 판단하여 제외
                    "post" = mongo_df$CommunityTabPostCount, "comment" = mongo_df$DiscussionCount, 
                    "desc" = mongo_df$AboutTab$DescSize, "totalView" = mongo_df$AboutTab$TotalViewCount,
                    "elapsed" = as.integer(Sys.Date() - as.Date(mongo_df$AboutTab$JoinDate, format = "%Y. %m. %d.")))
ch_df_fac <- data.frame("subs" = mongo_df$SubscriberNum, "category" = mongo_df$Category,  "main_video" = mongo_df$HomeTab$MainVideo, 
                        # 소통 자체가 활발하지 못해 무의미 하기 때문에 범주형 변수도 분석 대상에서 제외
                        "comm_disc" = as.factor(ifelse(mongo_df$CommunityVitalization == TRUE, "community", ifelse(mongo_df$DiscussionVitalization == TRUE, "discussion", "none"))),
                        "link" = as.factor(mongo_df$AboutTab$LinkCount), "section" = as.factor(mongo_df$HomeTab$Section))
str(ch_df_num)
str(ch_df_fac)
attach(ch_df_num)
attach(ch_df_fac)


# 3-2 이상치 그룹, 일반 그룹 데이터 프레임 생성
## 이상치 찾기
boxplot(subs)
summary(subs)
Q3 <- round(summary(subs)[[5]])
Q1 <- round(summary(subs)[[2]])
IQR = Q3 - Q1
outliers <- Q3 + 1.5 * IQR
## 이상치 그룹
outliers_df_num <- ch_df_num[subs >= outliers,]
names(outliers_df_num) <- c("Osubs", "Oplaylist", "Ovideo", "Odesc", "OtotalView", "Oelapsed")
outliers_df_fac <- ch_df_fac[subs >= outliers,]
names(outliers_df_fac) <- c("Osubs", "Ocategory", "Omain_video", "Olink", "Osection")
attach(outliers_df_num)
attach(outliers_df_fac)
## 일반 그룹
normal_df_num <- ch_df_num[subs < outliers,]
names(normal_df_num) <- c("Nsubs", "Nplaylist", "Nvideo", "Ndesc", "NtotalView", "Nelapsed")
normal_df_fac <- ch_df_fac[subs < outliers,]
names(normal_df_fac) <- c("Nsubs", "Ncategory", "Nmain_video", "Nlink", "Nsection")
attach(normal_df_num)
attach(normal_df_fac)
# 4. 데이터 분포 확인
# 4-1. 일변량
## 전체 그룹
summary(ch_df_num)
hist(subs, breaks = 200, freq = F, main = "Subscriber Count")
hist(post, breaks = 200, freq = F, main = "Post Count")
hist(comment, breaks = 100, freq = F, main = "Comment Count")
hist(playlist, breaks = 100, freq = F, main = "Playlist Count")
hist(video, breaks = 200, freq = F, main = "Video Count")
hist(desc, breaks = 100, freq = F, main = "Description Character Count")
hist(totalView, breaks = 200, freq = F, main = "TotalView Count")
hist(elapsed, breaks = 100, freq = F, main = "Elapsed Time")
plot(category, main = "Category")
plot(comm_disc, main = "Communication/Discussion")
plot(link, main = "Link Count")
plot(main_video, main = "Main Video")
plot(section, main = "Section Count")
## outliers 그룹
hist(Osubs, breaks = 100)
hist(Oplaylist, breaks = 100)
hist(Ovideo, breaks = 100)
hist(Odesc, breaks = 100)
hist(OtotalView, breaks = 100)
hist(Oelapsed, breaks = 100)
plot(Ocategory)
plot(Olink)
plot(Osection)
## normal 그룹
hist(Nsubs, breaks = 100)
hist(Nplaylist, breaks = 100)
hist(Nvideo, breaks = 100)
hist(Ndesc, breaks = 100)
hist(NtotalView, breaks = 100)
hist(Nelapsed, breaks = 100)
plot(Ncategory)
plot(Nlink)
plot(Nsection)

# 4-2. 이변량
plot(subs ~ main_video)
plot(Osubs ~ Omain_video)
plot(Nsubs ~ Nmain_video)
## 전체 그룹
plot(ch_df_num)
plot(ch_df_fac)
plot(subs ~ post, main = "Subscriber by Post")
plot(subs ~ comment, main = "subscriber by Comment")
plot(subs ~ playlist, main = "Subscriber by Playlist Count")
plot(subs ~ video, main = "Subscriber by Video Count")
plot(subs ~ desc, main = "Subscriber by Description Character Count")
plot(subs ~ totalView, main = "Subscriber by Total View Count")
plot(subs ~ elapsed, main = "Subscriber by Elapsed Time")
## outliers 그룹
plot(outliers_df_num)
plot(outliers_df_fac)
plot(Osubs ~ Oplaylist)
plot(Osubs ~ Ovideo)
plot(Osubs ~ Odesc)
plot(Osubs ~ OtotalView)
plot(Osubs ~ Oelapsed)
## normal 그룹
plot(normal_df_num)
plot(normal_df_fac)
plot(Nsubs ~ Nplaylist)
plot(Nsubs ~ Nvideo)
plot(Nsubs ~ Ndesc)
plot(Nsubs ~ NtotalView)
plot(Nsubs ~ Nelapsed)

# 5. 상관분석
library(corrgram)
corrgram(ch_df_num, upper.panel = panel.cor, cor.method = "spearman")
corrgram(outliers_df_num, upper.panel = panel.cor, cor.method = "spearman")
corrgram(normal_df_num, upper.panel = panel.cor, cor.method = "spearman")
summary(ch_df_num_spear_cor)
# 5-1. 스피어만 상관계수를 고려한 변수의 가중치 계산
library(FSelector)
spear.cor.rank <- rank.correlation(ch_df_num)
cutoff.k.percent(spear.cor.rank, 1)
# 5-2. 상관계수 유의성 검정
## 가설 수립(hypothesis building)
## H0 : 구독자 수와 각 변수들은 상관관계가 없다.(r = 0)
## H1 : 구독자 수와 각 변수들은 상관관계가 있다.(r != 0)
cor.test(ch_df_num$post, ch_df_num$subs, method = "spearman")
cor.test(ch_df_num$comment, ch_df_num$subs, method = "spearman")
cor.test(ch_df_num$playlist, ch_df_num$subs, method = "spearman")
cor.test(ch_df_num$video, ch_df_num$subs, method = "spearman")
cor.test(ch_df_num$desc, ch_df_num$subs, method = "spearman")
cor.test(ch_df_num$totalView, ch_df_num$subs, method = "spearman")
cor.test(ch_df_num$elapsed, ch_df_num$subs, method = "spearman")

# 6. 범주형 변수 통계량
# 6-1. 카테고리 변수
library(ggplot2)
library(doBy)
category_df <- summaryBy(subs ~ category, ch_df_fac, FUN = summary)
category_df <- cbind(category_df, "N" = summary(category))
category_df <- cbind(category_df, "1st Qu_alpha" = round(category_df$`subs.1st Qu.`/category_df$N,2))
category_df <- cbind(category_df, "median_alpha" = round(category_df$subs.Median/category_df$N,2))
category_df <- cbind(category_df, "beta" = round((category_df$median_alpha - category_df$`1st Qu_alpha`) * category_df$`1st Qu_alpha`,2))
category_df
## 카테고리별 median값 시각화
ggplot() + geom_point(mapping= aes(1:nrow(category_df), category_df$subs.Median), shape = 21, col = "red", fill = "red") + geom_line(mapping = aes(1:nrow(category_df), category_df$subs.Median), col = "red")  + geom_point(mapping = aes(1:nrow(category_df), category_df$`subs.1st Qu.`), shape = 21, col = "blue", fill = "blue") + geom_line(mapping = aes(1:nrow(category_df), category_df$`subs.1st Qu.`), col = "blue") + xlab("category") + ylab("median(subs)") + scale_x_continuous(breaks = c(1:nrow(category_df)), labels = category_df$category)
## 카테고리별 채널 수 시각화
ggplot() + geom_bar(mapping = aes(1:nrow(category_df), category_df$N), stat = "identity") + scale_x_continuous(breaks = c(1:nrow(category_df)), labels = category_df$category) + xlab("category") + ylab("N")
## 카테고리별 채널 수를 고려한 분위수값 시각화
ggplot() + geom_point(mapping = aes(1:nrow(category_df), category_df$`1st Qu_alpha`), shape = 21, col = "blue", fill = "blue") + geom_line(mapping = aes(1:nrow(category_df), category_df$`1st Qu_alpha`), col = "blue") + geom_point(mapping = aes(1:nrow(category_df), category_df$median_alpha), shape = 21, col = "red", fill = "red") + geom_line(mapping = aes(1:nrow(category_df), category_df$median_alpha), col = "red") + geom_point(mapping = aes(1:nrow(category_df), category_df$`1st Qu_alpha`), shape = 21, col = "blue", fill = "blue") + geom_line(mapping = aes(1:nrow(category_df), category_df$`1st Qu_alpha`), col = "blue") + scale_x_continuous(breaks = c(1:nrow(category_df)), labels = category_df$category) + xlab("category") + ylab("α")
## 들어가기 좋은 카테고리 점수화 (α(median) - α(1st qu.))*α(1st qu.)
ggplot() + geom_point(mapping = aes(1:nrow(category_df), category_df$beta), shape = 21, col = "purple", fill = "purple") + geom_line(mapping = aes(1:nrow(category_df), category_df$beta), col = "purple") + scale_x_continuous(breaks = c(1:nrow(category_df)), labels = category_df$category) + xlab("category") + ylab("β")


# 6-2. 메인비디오 변수
main_video_df <- summaryBy(subs ~ main_video, ch_df_fac, FUN = summary)
main_video_df <- cbind(main_video_df, "N" = c(table(main_video)[[1]], table(main_video)[[2]]))
main_video_df <- cbind(main_video_df, "alpha" = round(main_video_df$subs.Median/main_video_df$N,2))
main_video_df
ggplot(ch_df_fac, aes(main_video, subs)) + geom_point() + annotate("text", x = 1.1, y = median_false, label = paste("median=\n", median_false)) + annotate("text", x = 2.1, y = median_true, label = paste("median=\n", median_true))


# 6-3. 링크 수 변수
ch_df_fac
link_df <- summaryBy(subs ~ link, ch_df_fac, FUN = summary)
link_df <- cbind(link_df, "N" = summary(link))
link_df <- cbind(link_df, "1st_alpha" = round(link_df$`subs.1st Qu.`/link_df$N,2))
link_df <- cbind(link_df, "median_alpha" = round(link_df$subs.Median/link_df$N,2))
link_df <- cbind(link_df, "1st_log" = round(log(link_df$`1st_alpha` + 1),2))
link_df <- cbind(link_df, "median_log" = round(log(link_df$median_alpha + 1),2))
link_df
## α 값 시각ㅎ
ggplot() + geom_point(mapping = aes(1:nrow(link_df), link_df$median_alpha), shape = 21, col = "red", fill = "red") + geom_line(mapping = aes(1:nrow(link_df), link_df$median_alpha), col = "red") + geom_point(mapping = aes(1:nrow(link_df), link_df$`1st_alpha`), shape = 21, col = "blue", fill = "blue") + geom_line(mapping = aes(1:nrow(link_df), link_df$`1st_alpha`), col = "blue") + scale_x_continuous(breaks = c(1:nrow(link_df)), labels = link_df$link) + xlab("link") + ylab("α")
## log(α) 값 시각화
ggplot() + geom_point(mapping = aes(1:nrow(link_df), link_df$median_log), shape = 21, col = "red", fill = "red") + geom_line(mapping = aes(1:nrow(link_df), link_df$median_log), col = "red") + geom_point(mapping = aes(1:nrow(link_df), link_df$`1st_log`), shape = 21, col = "blue", fill = "blue") + geom_line(mapping = aes(1:nrow(link_df), link_df$`1st_log`), col = "blue") + scale_x_continuous(breaks = c(1:nrow(link_df)), labels = link_df$link) + xlab("link") + ylab("log(α)")
## 채널 수 
ggplot() + geom_bar(mapping = aes(1:nrow(link_df), link_df$N), stat = "identity") + scale_x_continuous(breaks = c(1:nrow(link_df)), labels = link_df$link) + xlab("link") + ylab("N")


# 6-4. 홈 섹션 변수
section_df <- summaryBy(subs ~ section, ch_df_fac, FUN = summary)
section_df <- cbind(section_df, "N" = summary(section))
section_df <- cbind(section_df, "1st_alpha" = round(section_df$`subs.1st Qu.`/section_df$N,2))
section_df <- cbind(section_df, "median_alpha" = round(section_df$subs.Median/section_df$N,2))
section_df <- cbind(section_df, "1st_log" = round(log(section_df$`1st_alpha`),2))
section_df <- cbind(section_df, "median_log" = round(log(section_df$median_alpha),2))
section_df
# α 값 시각화
ggplot() + geom_point(mapping = aes(1:nrow(section_df), section_df$median_alpha), shape = 21, col = "red", fill = "red") + geom_line(mapping = aes(1:nrow(section_df), section_df$median_alpha), col = "red") + geom_point(mapping = aes(1:nrow(section_df), section_df$`1st_alpha`), shape = 21, col = "blue", fill = "blue") + geom_line(mapping = aes(1:nrow(section_df), section_df$`1st_alpha`), col = "blue") + scale_x_continuous(breaks = c(1:nrow(section_df)), labels = section_df$section) + xlab("section") + ylab("α")
# log(α) 값 시각화
ggplot() + geom_point(mapping = aes(1:nrow(section_df), section_df$median_log), shape = 21, col = "red", fill = "red") + geom_line(mapping = aes(1:nrow(section_df), section_df$median_log), col = "red") + geom_point(mapping = aes(1:nrow(section_df), section_df$`1st_log`), shape = 21, col = "blue", fill = "blue") + geom_line(mapping = aes(1:nrow(section_df), section_df$`1st_log`), col = "blue") + scale_x_continuous(breaks = c(1:nrow(section_df)), labels = section_df$section) + xlab("section") + ylab("log(α)")
# 홈 섹션별 채널 수
ggplot() + geom_bar(mapping = aes(1:nrow(section_df), section_df$N), stat = "identity") + scale_x_continuous(breaks = c(1:nrow(section_df)), labels = section_df$section) + xlab("section") + ylab("N")