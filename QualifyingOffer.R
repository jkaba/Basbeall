# Name: Jameel Kaba

# Load Libraries
library(rvest)
library(readr)
library(tidyverse)

# Scrape data
data <- read_html("#Insert Data URL/.csv file here")
tables <- data %>% html_table(fill = TRUE)

# Turn list into table
tables <- do.call(rbind.data.frame, tables)
tables <- tables %>% rename(Player = X1, Salary = X2,Year = X3, Level = X4)

# Remove blanks and no salary data
tables <- tables[-which(tables$Salary=="" | tables$Salary=="no salary data"),] 

# Arrange table from highest to lowest while converting salaries into integers
tables <- tables[order(parse_number(tables$Salary), decreasing = TRUE),]

# Take the highest 125 salaries
tables <- head(tables, 125)

# Save the highest 125 salaries as a .csv for reference
print("The top 125 Salaries are saved as top125_salaries.csv")
write_csv(tables, "top125_salaries.csv")

# calculate and return the qualifying offer
qualifying_offer <- mean(parse_number(tables$Salary))
sprintf("The upcoming Qualifying Offer is set at $%s", formatC(qualifying_offer, format="d", big.mark=","))
