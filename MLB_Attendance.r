# Data will be scraped from the following links
# Data will be from 1998-2019; We want data starting when the league expanded to 30
# Attendance: http://www.baseball-reference.com/leagues/MLB/1990-misc.shtml
# Standings: http://www.baseball-reference.com/leagues/MLB/1990-standings.shtml
# Pitching: http://www.baseball-reference.com/leagues/MLB/1990-standard-pitching.shtml
# Fielding: http://www.baseball-reference.com/leagues/MLB/1990-standard-fielding.shtml
# Batting: http://www.baseball-reference.com/leagues/MLB/1990-standard-batting.shtml
# Author = Jameel Kaba

# Load libraries
library(XML)
library(ggplot2)
library(plyr)
library(dplyr)
library(car)
library(data.table)
library(stringr)
library(alluvial)
library (glmnet)

# Scrape data (attendance)
fetch_attendance <- function(year) {
  url <- paste0("http://www.baseball-reference.com/leagues/MLB/", year, "-misc.shtml")
  data <- readHTMLTable(url, stringsAsFactors = FALSE)
  data <- data[[1]]
  data$year <- year
  data
}

attendance <- ldply(1998:2019, fetch_attendance, .progress="text")

# Scrape data (standings)
fetch_standings <- function(year1) {
  url1 <- paste0("http://www.baseball-reference.com/leagues/MLB/", year1, "-standings.shtml")
  data1 <- readHTMLTable(url1, stringsAsFactors = FALSE)
  data1 <- data1[[2]]
  data1$year1 <- year1
  data1
}

standings <- ldply(1998:2019, fetch_standings, .progress="text")

# Scrape data (Pitching)
fetch_pitching <- function(year2) {
  url2 <- paste0("http://www.baseball-reference.com/leagues/MLB/", year2, "-standard-pitching.shtml")
  data2 <- readHTMLTable(url2, stringsAsFactors = FALSE)
  data2 <- data2[[1]]
  data2$year2 <- year2
  data2
}

pitching <- ldply(1998:2019, fetch_pitching, .progress="text")

# Scrape data (Fielding)
fetch_fielding <- function(year3) {
  url3 <- paste0("http://www.baseball-reference.com/leagues/MLB/", year3, "-standard-fielding.shtml")
  data3 <- readHTMLTable(url3, stringsAsFactors = FALSE)
  data3 <- data3[[1]]
  data3$year3 <- year3
  data3
}

fielding <- ldply(1998:2019, fetch_fielding, .progress="text")

# Scrape data (batting)
fetch_batting <- function(year4) {
  url4 <- paste0("http://www.baseball-reference.com/leagues/MLB/", year4, "-standard-batting.shtml")
  data4 <- readHTMLTable(url4, stringsAsFactors = FALSE)
  data4 <- data4[[1]]
  data4$year4 <- year4
  data4
}

batting <- ldply(1998:2019, fetch_batting, .progress="text")

# Now that all the data has been scraped we need to merge them together
# Data will be merged on team name and the year

# Change column names to year (Clean up data)
names(standings)[24]<-"year"
names(pitching)[37]<-"year"
names(fielding)[17]<-"year"
names(batting)[30]<-"year"

# Merge data frames on team name and year
# Due to restrictions we can only merge two data frames at a time
teams_data <- merge(standings, attendance, by=c("Tm", "year"))
teams_data2 <- merge(teams_data, batting, by=c("Tm", "year"))
teams_data3 <- merge(teams_data2, fielding, by=c("Tm", "year"))
teams_data4 <- merge(teams_data3, pitching, by=c("Tm", "year"))

# Teams have changed their names over the years and some even cities
teams_counts <- aggregate(year ~ Tm, data = teams_data4, length)
print(teams_counts)
teams_counts[order(teams_counts$year),]

# Remove duplicate columns in order to continue
teams_data4 <- teams_data4[c(-71,-92)]

# Montreal Expos -> Washington Nationals 2005
teams_data5 <- mutate(teams_data4, Tm = recode(Tm, "'MON'='WSN'"))

# Florida Marlins -> Miami Marlins 2012
teams_data5 <- mutate(teams_data5, Tm = recode(Tm, "'FLA'='MIA'"))

# Tampa Bay Devil Rays -> Tampa Bay Rays 2008
teams_data5 <- mutate(teams_data5, Tm = recode(Tm, "'TBD'='TBR'"))

# Anaheim Angels -> Los Angeles Angels 2004
teams_data5 <- mutate(teams_data5, Tm = recode(Tm, "'ANA'='LAA'"))

# Check data to ensure all teams have correct amount of data
teams_counts1 <- aggregate(year ~ Tm, data = teams_data5, length)
print(teams_counts1)

# Inspect data to ensure all is well
str(teams_data5)

# Because R has problems with commas, we need to replace them with spaces
remove_commas <- function(x) {
  x <- str_replace_all(x, ",", "") 
}

teams_data5$Attendance <- remove_commas(teams_data5$Attendance)

# All columns will be read as characters, we need to make the numeric columns numeric
columns <- subset(teams_data5, select = c(5:13, 25:33, 40:81, 84:117))
teams <- data.frame(sapply(columns, as.numeric))
teams_other <- subset(teams_data5, select = c(-5:-13, -25:-33, -40:-81, -84:-117))
teams_final <- data.frame(teams, teams_other)

# We're going to add a column to the data frame which
#  identifies what quartile in terms of wins that teams will fall under
setDT(teams_final)
teams_final[,wins_quartile:=cut(W.x,
                      breaks=quantile(W.x,probs=seq(0,1,by=1/4)),
                      labels=1:4,right=F)]

str(teams_final$wins_quartile)

# Develop dot plot charts
# 1. Wins per season
ggplot(teams_final)+ geom_point(aes(x=Tm, y=W.x), colour = "blue") +
  coord_flip() + ggtitle("Single Season Win Totals") + 
  xlab("Team") + ylab("Wins")

# 2. Total wins
wins_total <- aggregate(W.x ~ Tm, data = teams_final, sum) 
wins_total1$Tm <-factor(wins_total$Tm, levels=wins_total[order(wins_total$W.x), "Tm"])

ggplot(wins_total1)+ geom_point(aes(x=Tm, y=W.x), colour = "blue") +
  coord_flip() + ggtitle("Win Totals from 1998-2019") +
  xlab("Team") + ylab("Wins")

# 3. Total Home Runs
hr_total <- aggregate(HR.x ~ Tm, data = teams_final, sum) 
hr_total$Tm <-factor(hr_total$Tm, levels=hr_total[order(hr_total$HR.x), "Tm"])

ggplot(hr_total)+ geom_point(aes(x=Tm, y=HR.x), colour = "blue") +
  coord_flip() + ggtitle("Home Run Totals from 1998-2019") +
  xlab("Team") + ylab("Home Runs")

# 4. Total Stolen Bases
sb_total <- aggregate(SB ~ Tm, data = teams_final, sum) 
sb_total$Tm <-factor(sb_total$Tm, levels=sb_total[order(sb_total$SB), "Tm"])

ggplot(sb_total)+ geom_point(aes(x=Tm, y=SB), colour = "blue") +
  coord_flip() + ggtitle("Stolen Base Totals from 1998-2019") +
  xlab("Team") + ylab("Stolen Bases")

# 5. Total Errors
e_total <- aggregate(E ~ Tm, data = teams_final, sum) 
e_total$Tm <-factor(e_total$Tm, levels=e_total[order(e_total$E), "Tm"])

ggplot(e_total)+ geom_point(aes(x=Tm, y=E), colour = "blue") +
  coord_flip() + ggtitle("Error Totals from 1998-2019") +
  xlab("Team") + ylab("Errors")

# 6. Total Earned Runs
er_total <- aggregate(ER ~ Tm, data = teams_final, sum) 
er_total$Tm <-factor(er_total$Tm, levels=er_total[order(er_total$ER), "Tm"])

ggplot(er_total)+ geom_point(aes(x=Tm, y=ER), colour = "blue") +
  coord_flip() + ggtitle("Earned Run Totals from 1998-2019") +
  xlab("Team") + ylab("Earned Runs")

# Creating an Alluvial plot
wins_over_time <- subset(teams_final, select = c(95,96,2))
selected_teams <- filter(wins_over_time, Tm == "NYY" | Tm == "ATL" | Tm == "STL" 
                         | Tm == "SFG" | Tm == "BOS" | Tm == "TEX")

alluvial_ts(selected_teams, title = "Wins over Time")

# Now that the data is formed, let's try to see what impacts attendance

# We're going to start by taking columns which can be considered as predictive
teams_subset <- subset(teams_final, select = c(10,2,12,13,17,25,34,56,73,77,95))
summary(teams_subset)
teams_subset$Tm <- as.factor(as.character(teams_subset$Tm))

# For contextual purposes sum the attendance column
sum(teams_subset$Attendance)

# Break data into training and test sets
set.seed(10)
train = sample(1: nrow(x), nrow(x)/2)
test = (-train )
y.test = y[test]

# Ordinary Least Squares
pairs(teams_subset)
ols_model <- lm(Attendance ~ 0 + W.x + BatAge.x + PAge.x + X.A.S +
                  R.y + SO.x + E + SV + ER + Tm, data=teams_subset)
plot(ols_model)
summary(ols_model)
vif(ols_model)

# Issues arrise with multi-collinearity move to Ridge regression
# Ridge regression
# Create matrices which are needed for the glmnet package
x <- model.matrix (Attendance ~.,teams_subset )[,-1]
y=teams_subset$Attendance

# Run the ridge regression model
ridge_model = glmnet(x[train,], y[train], alpha = 0)

# Use cross-validation to determine what the best value is for lambda
cv.out = cv.glmnet(x[train,], y[train], alpha = 0)
plot(cv.out)
bestlam = cv.out$lambda.min
bestlam

# Run the ridge regression on the full dataset using the best lambda
# View the coefficients of the model
out = glmnet(x,y,alpha =0)
ridge.coef = predict(out, type ="coefficients", s=bestlam)
ridge.coef

# Lasso regression
# Follow the same process as above, except alpha is set to 1

# Run the lasso regression model
lasso_model = glmnet(x[train,], y[train], alpha = 1)

# Use cross-validation to determine the best value for lambda
cv.out1 = cv.glmnet(x[train,], y[train], alpha = 1)
plot(cv.out1)
bestlam1 = cv.out$lambda.min
bestlam1

# Run the lasso regression on the full dataset using the best lambda
# View the coefficients of the model
out1 = glmnet(x,y,alpha = 1)
lasso.coef = predict(out1, type ="coefficients", s=bestlam1)
lasso.coef

# MSE of the Ordinary Least Squares
# Set lambda = 0
ols_pred = predict(ridge.mod ,s=0, newx=x[test,], exact=T)
ols_mse <- mean((ols_pred -y.test)^2)
print(ols_mse)
sqrt(ols_mse)

# MSE of the Ridge Regression
ridge.pred = predict(ridge_model,s=bestlam ,newx=x[test ,])
ridge_mse <- mean((ridge.pred-y.test)^2)
print(ridge_mse)
sqrt(ridge_mse)

# MSE of the Lasso Regression
lasso.pred = predict(lasso_model,s=bestlam ,newx=x[test ,])
lasso_mse <- mean((lasso.pred-y.test)^2)
print(lasso_mse)
sqrt(lasso_mse)

