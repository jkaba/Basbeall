# R script to take a look at Justin Verlander's no hitter against the Jays on 9/1/2019
# Author = Jameel Kaba

# Load in XML library
library(XML)

# Scrape and save the data from brooksbaseball
# Data is saved as a .csv to avoid char reading issue
verlander <-htmlParse("http://www.brooksbaseball.net/pfxVB/tabdel_expanded.php?pitchSel=434378&game=gid_2019_09_01_houmlb_tormlb_1/&s_type=&h_size=700&v_size=500")
verlander.tab<-readHTMLTable(verlander, stringsAsFactors=FALSE)
verlander.df<-verlander.tab[[1]]
write.csv(verlander.df, file = "Verlander.csv")

# Reading in the .csv, and producing a summary
verlander <- read.csv("verlander.csv")
summary(verlander)

# 1. Let's start by taking a look at Verlander's pitch speed throughout the game
plot(ecdf(verlander$start_speed),
     main = "Cumulative Distribution of Pitch Speed",
     ylab = "Cumulative Proportion",
     xlab = "Pitch Speed",
     yaxt = "n")
axis (side=2, at=seq(0, 1, by=0.1), las=1, labels=paste(seq(0, 100, by=10),
                                                            "%", sep=" "))
abline(h=0.9, lty=3)
abline(v=quantile(verlander$start_speed, pr=0.9), lty=3)

# 2. Now let's take a peek at the movement for the pitches
library(ggplot2)
p <- ggplot(verlander, aes(x=pfx_x, y=pfx_z))
p + geom_point() + stat_density2d() + ggtitle("Density of Vertical and Hortizontal Pitch Movement")

# 3. To better understand the pitches, let's visualize the pitches based on velocity, movement, and spin
ggplot(verlander, aes(start_speed, fill = mlbam_pitch_name)) +
  geom_histogram(binwidth = 1) + facet_wrap(~ mlbam_pitch_name) +
  ggtitle("Pitch Speed Histogram by Pitch Type")

ggplot(verlander, aes(x=pfx_x, y=pfx_z)) +
  geom_point(shape=19) + facet_wrap(~ mlbam_pitch_name) +  
  geom_smooth() + ggtitle("Vertical and Horizontal Movement by Pitch")

ggplot(verlander, aes(spin, fill = mlbam_pitch_name)) +
  geom_density() + facet_wrap(~ mlbam_pitch_name) +
  ggtitle("Spin by Pitch Type")

# 4. Lets break the data by different results to see if it shows a pattenr
ball <- subset(verlander, pdes == "Ball")
called_strike <- subset(verlander, pdes == "Called Strike")
foul <- subset(verlander, pdes == "Foul")
in_play_outs <- subset(verlander, pdes == "In play, out(s)")
swinging_strike <- subset(verlander, pdes == "Swinging Strike")

# Making summaries in regards to outcomes
summary(ball)
summary(called_strike)
summary(foul)
summary(in_play_outs)
summary(swinging_strike)

#5. Look at Verlander's performance throughout the game
mean(verlander$start_speed)
aggregate(start_speed ~ inning + mlbam_pitch_name, data = verlander, mean)

p1 <- ggplot(verlander, aes(x=inning, y=mlbam_pitch_name, fill=start_speed))
p1 + geom_tile() + scale_fill_gradient2(midpoint=92, low="blue", high="red") +
  ggtitle("Pitch Speed by Inning") + 
  scale_x_continuous(breaks = c(1,2,3,4,5,6,7,8,9))

library(dplyr)
early <- filter(verlander, inning == 1 | inning == 2 | inning == 3 )
mid <- filter(verlander, inning == 4 | inning == 5 | inning == 6 )
late <- filter(verlander, inning == 7 | inning == 8 | inning == 9 )

summary(early)
prop.table(table(early$mlbam_pitch_name))
mean(early$start_speed)

summary(mid)
prop.table(table(mid$mlbam_pitch_name))
mean(mid$start_speed)

summary(late)
summary(mid)
prop.table(table(late$mlbam_pitch_name))
mean(late$start_speed)
