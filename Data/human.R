raw_data <- read.csv(file = "raw_2by2.csv")
library(lme4)
library(lmerTest)

raw_data$period <- as.factor(raw_data$period)
raw_data$boundary <- as.factor(raw_data$boundary)
raw_data$window_size <- as.factor(raw_data$window_size)
raw_data$window_weight <- as.factor(raw_data$window_weight)
raw_data$window_type <- as.factor(raw_data$window_type)
raw_data$normalization <- as.factor(raw_data$normalization)
raw_data$encode <- as.factor(raw_data$encode)
raw_data$representation <- as.factor(raw_data$representation)
raw_data$run <- as.factor(raw_data$run)

performance_mixed <- lmer(performance ~ encode + representation + encode * representation + (1 | run), data = raw_data)
summary(performance_mixed)
anova(performance_mixed)

rep <- as.numeric(raw_data$representation == 'space')
encode <- as.numeric(raw_data$encode == 'sim')
cor.test(rep,raw_data$performance)
cor.test(encode,raw_data$performance)
