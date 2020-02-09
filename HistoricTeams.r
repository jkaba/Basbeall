# Analysis on Teams throughout the years
# Analysis methods: correlation matrix, relationship between variables, parallel coordinate plots, 
#                   K means Clustering, hierarchical structure (dendrogram)
# Author = Jameel

# Load in the libraries and data
#https://cran.r-project.org/web/packages/Lahman/Lahman.pdf 
library(Lahman) 
library(cluster)
library(corrplot)
library(gplots)
library(hexbin)
library(ggplot2)
library(MASS)
library(colorRamps)

#http://rpackages.ianhowson.com/rforge/Lahman/man/Teams.html 
data(Teams) 

# Let's get a summary of the data and see what we have
summary(Teams)

# We need to isolate selected variables
teams_subset <- Teams[c(7, 15:23, 27:28, 30:32, 34:38)] 

# Create a team reference which has name and season
teams_reference <- Teams[c(1, 4, 7, 15:23, 27:28, 30:32, 33:38)] 

# Teams with missing values are removed for simplicity
teams_subset <- na.omit(teams_subset)
teams_reference <- na.omit(teams_reference)

# Clean up the team reference so that it only has the team name and season
teams_reference <- teams_reference[c(1:2)]

# Converting each variable to be on a per-game basis rather than per season, done due to unequal number of games
teams_final <- sweep(teams_subset,1,unlist(teams_subset[,1]),"/")

# Print out the summary with the per game data
summary(teams_final)

# Remove number of games played from the data as we've converted to per game
teams_final <- teams_final[(-1)]

# Create a correlation matrix to get an idea in regards to how the game has changed over the years
correlations <- cor(teams_final)
correlations <- round(correlations, digits=2)
corrplot(correlations, method="shade", shade.col=NA, tl.col="black")

# Lets look at the relationship between select variables

# 1. Relationship between Errors and Runs Allowed
p <- ggplot(teams_final, aes(x=E, y=RA))
p + stat_binhex() +
  scale_fill_gradient(low="lightblue", high="red") +
  ggtitle("Relationship Between Errors Per Game \n and Runs Allowed Per Game")

# 2. Relationship between Home Runs and Runs per game
p1 <- ggplot(teams_final, aes(x=HR, y=R))
p1 + stat_binhex() +
  scale_fill_gradient(low="lightblue", high="red") +
  ggtitle("Relationship Between HR Per Game \n and Runs Per Game")

# Let's try to go further and make some parallel coordinate plots 
c <- blue2red(100)

# 1. Start with hitting, focus will be around number of Home Runs
h <- cut(teams_final$HR, 100)
parcoord(teams_final, col=c[as.numeric(h)])

# 2. Let's look into pitching, focus being on shutouts
r <- cut(teams_final$SHO, 100)
parcoord(teams_final, col=c[as.numeric(r)])

# Time for K Means CLustering
teams_scaled <- scale(teams_final)

# 6 Clusters for K means
set.seed(500)
fit1 <- kmeans(teams_final, 6, nstart=25) 

# Make a PCA Plot to visualize the Clustering
set.seed(500)
clusplot(teams_scaled, fit1$cluster, color=TRUE, shade=TRUE,
         labels=2, lines=0, main = "PCA Plot of K-Means Cluster")

# Let's break the data into respective clusters
teams_final <- data.frame(teams_final, fit1$cluster)
cluster1 <- teams_final[which(teams_final$fit1.cluster=='1'),]
cluster2 <- teams_final[which(teams_final$fit1.cluster=='2'),]
cluster3 <- teams_final[which(teams_final$fit1.cluster=='3'),]
cluster4 <- teams_final[which(teams_final$fit1.cluster=='4'),]
cluster5 <- teams_final[which(teams_final$fit1.cluster=='5'),]
cluster6 <- teams_final[which(teams_final$fit1.cluster=='6'),]

# Let's take a look at summaries for each group
summary(cluster1)
summary(cluster2)
summary(cluster3)
summary(cluster4)
summary(cluster5)
summary(cluster6)

# Combine the clusters with their teams
teams_reference <- data.frame(teams_reference, fit1$cluster)
group1 <- teams_reference[which(teams_reference$fit1.cluster=='1'),]
group2 <- teams_reference[which(teams_reference$fit1.cluster=='2'),]
group3 <- teams_reference[which(teams_reference$fit1.cluster=='3'),]
group4 <- teams_reference[which(teams_reference$fit1.cluster=='4'),]
group5 <- teams_reference[which(teams_reference$fit1.cluster=='5'),]
group6 <- teams_reference[which(teams_reference$fit1.cluster=='6'),]
team_clusters <- rbind(group1, group2, group3, group4, group5, group6)

# Save the results
write.csv(team_clusters, file = "Team Clustering Results.csv")

# Print out team contents of group 1
print(group1)
group1$yearID <- as.factor(as.integer(group1$yearID))
summary(group1, 50)

# Print out team contents of group 2
print(group2)
group2$yearID <- as.factor(as.integer(group2$yearID))
summary(group2, 50)

# Print out team contents of group 3
print(group3)
group3$yearID <- as.factor(as.integer(group3$yearID))
summary(group3, 50)

# Print out team contents of group 4
print(group4)
group4$yearID <- as.factor(as.integer(group4$yearID))
summary(group4, 50)

# Print out team contents of group 5
print(group5)
group5$yearID <- as.factor(as.integer(group5$yearID))
summary(group5, 50)

# Print out team contents of group 6
print(group6)
group6$yearID <- as.factor(as.integer(group6$yearID))
summary(group6, 50)

# Making a dendogram for heirarchical cluster, looks just a little messy
set.seed(100)
teams_hclust <- teams_scaled
dm = dist(teams_hclust,method="euclidean")
hclust_teams <- hclust(dm, method="complete")
plot(hclust_teams)

# Let's zoom in on the dendrogram
plot(cut(as.dendrogram(hclust_teams), h=4)$lower[[30]])

# Let's compare how similar each pair of teams are and find out who they are

# 1516: 1974 San Diego Padres
# 1823: 1986 Seattle Mariners
teams_hclust[c(1516, 1823),]
teams_reference[c(1516, 1823),]

# 1427: 1971 California Angels
# 1533: 1975 Milwaukee Brewers
teams_hclust[c(1427, 1533),]
teams_reference[c(1427, 1533),]

# 1601: 1978 Cleveland Indians
# 1825: 1986 St. Louis Cardinals
teams_hclust[c(1601, 1825),]
teams_reference[c(1601, 1825),]

# 1402: 1970 Boston Red Sox
# 2100: 1997 Chicago White Sox
teams_hclust[c(1402, 2100),]
teams_reference[c(1402, 2100),]

# 1607: 1978 Milwaukee Brewers
# 2007: 1993 Seattle Mariners
teams_hclust[c(1607, 2007),]
teams_reference[c(1607, 2007),]