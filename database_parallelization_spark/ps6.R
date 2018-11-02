dir = '/global/scratch/paciorek/wikistats_full/dated_for_R'
files = list.files(dir)

require(parallel) # one of the core R packages require(doParallel)

## Loading required package: ## Loading required package: ## Loading required package:
require(doParallel)
library(foreach)
library(readr)

nCores <- detectCores()
registerDoParallel(nCores)

nSub <- 960

system.time(
result <- foreach(i = 1:nSub) %dopar% {
  lines <- read_delim(file = paste(dir,files[i],sep='/'),
                             delim=' ',quote="",col_name=FALSE)
  match_index = grep('Barack_Obama',lines$X4)
  lines[match_index,] # this will become part of the out object 
})

result_df <- do.call(rbind.data.frame, result)
write.table(result_df,'result.txt', sep="\t",
            col.names = FALSE, row.names = FALSE)