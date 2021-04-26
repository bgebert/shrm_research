setwd("/Users/bgebert/Scripts/SHRM/membership_roster_prep/")
library(tidyverse)
library(descr)
library(lubridate)
library(readxl)

#FUNCTIONS

cleanState <- function(cntry,st){
    if(is.na(st)|is.na(cntry)) NA
    else if(cntry!= "United States"& cntry!="US Minor Outlying Islands"&
            cntry!="Virgin Islands (USA)"&cntry!="American Samoa"&
            cntry!="Guam"&cntry!="Northern Mariana Islands"&
            cntry!="Marshall Islands"&cntry!="Micronesia, Federal State of"&
            cntry!="Palau") NA
    else if(st=="Alaska"|st=="AK") "AK"
    else if(st=="Alabama"|st=="AL") "AL"
    else if(st=="Arkansas"|st=="AR") "AR"
    else if(st=="Arizona"|st=="AZ") "AZ"
    else if(st=="California"|st=="CA") "CA"
    else if(st=="Colorado"|st=="CO") "CO"
    else if(st=="Connecticut"|st=="CT") "CT"
    else if(st=="District of Columbia"|st=="DC") "DC"
    else if(st=="Delaware"|st=="DE") "DE"
    else if(st=="Florida"|st=="FL") "FL"
    else if(st=="Georgia"|st=="GA") "GA"
    else if(st=="Hawaii"|st=="HI") "HI"
    else if(st=="Iowa"|st=="IA") "IA"
    else if(st=="Idaho"|st=="ID") "ID"
    else if(st=="Illinois"|st=="IL") "IL"
    else if(st=="Indiana"|st=="IN") "IN"
    else if(st=="Kansas"|st=="KS") "KS"
    else if(st=="Kentucky"|st=="KY") "KY"
    else if(st=="Louisiana"|st=="LA") "LA"
    else if(st=="Massachusetts"|st=="MA") "MA"
    else if(st=="Maryland"|st=="MD") "MD"
    else if(st=="Maine"|st=="ME") "ME"
    else if(st=="Michigan"|st=="MI") "MI"
    else if(st=="Minnesota"|st=="MN") "MN"
    else if(st=="Missouri"|st=="MO") "MO"
    else if(st=="Mississippi"|st=="MS") "MS"
    else if(st=="Montana"|st=="MT") "MT"
    else if(st=="North Carolina"|st=="NC") "NC"
    else if(st=="North Dakota"|st=="ND") "ND"
    else if(st=="Nebraska"|st=="NE") "NE"
    else if(st=="New Hampshire"|st=="NH") "NH"
    else if(st=="New Jersey"|st=="NJ") "NJ"
    else if(st=="New Mexico"|st=="NM") "NM"
    else if(st=="Nevada"|st=="NV") "NV"
    else if(st=="New York"|st=="NY") "NY"
    else if(st=="Ohio"|st=="OH") "OH"
    else if(st=="Oklahoma"|st=="OK") "OK"
    else if(st=="Oregon"|st=="OR") "OR"
    else if(st=="Pennsylvania"|st=="PA") "PA"
    else if(st=="Rhode Island"|st=="RI") "RI"
    else if(st=="South Carolina"|st=="SC") "SC"
    else if(st=="South Dakota"|st=="SD") "SD"
    else if(st=="Tennessee"|st=="TN") "TN"
    else if(st=="Texas"|st=="TX") "TX"
    else if(st=="Utah"|st=="UT") "UT"
    else if(st=="Virginia"|st=="VA") "VA"
    else if(st=="Vermont"|st=="VT") "VT"
    else if(st=="Washington"|st=="WA") "WA"
    else if(st=="Wisconsin"|st=="WI") "WI"
    else if(st=="West Virginia"|st=="WV") "WV"
    else if(st=="Wyoming"|st=="WY") "WY"
    else if(st=="Wyoming"|st=="WY") "WY"    
    else if(st=="American Samoa"|st=="AS") "AS"
    else if(st=="Federated sts of Micronesia"|st=="FM") "FM"
    else if(st=="Guam"|st=="GU") "GU"
    else if(st=="Marshall Islands"|st=="MH") "MH"
    else if(st=="Northern Mariana Islands"|st=="MP") "MP"
    else if(st=="Palau"|st=="PW") "PW"
    else if(st=="Puerto Rico"|st=="PR") "PR"
    else if(st=="Virgin Islands"|st=="VI") "VI"
    else NA
}

findRegion <- function(state){
    if(is.na(state)) NA
    else if(state=="Alaska"|state=="AK") "West"
    else if(state=="Alabama"|state=="AL") "South"
    else if(state=="Arkansas"|state=="AR") "South"
    else if(state=="Arizona"|state=="AZ") "West"
    else if(state=="California"|state=="CA") "West"
    else if(state=="Colorado"|state=="CO") "West"
    else if(state=="Connecticut"|state=="CT") "Northeast"
    else if(state=="District of Columbia"|state=="DC") "South"
    else if(state=="Delaware"|state=="DE") "South"
    else if(state=="Florida"|state=="FL") "South"
    else if(state=="Georgia"|state=="GA") "South"
    else if(state=="Hawaii"|state=="HI") "West"
    else if(state=="Iowa"|state=="IA") "Midwest"
    else if(state=="Idaho"|state=="ID") "West"
    else if(state=="Illinois"|state=="IL") "Midwest"
    else if(state=="Indiana"|state=="IN") "Midwest"
    else if(state=="Kansas"|state=="KS") "Midwest"
    else if(state=="Kentucky"|state=="KY") "South"
    else if(state=="Louisiana"|state=="LA") "South"
    else if(state=="Massachusetts"|state=="MA") "Northeast"
    else if(state=="Maryland"|state=="MD") "South"
    else if(state=="Maine"|state=="ME") "Northeast"
    else if(state=="Michigan"|state=="MI") "Midwest"
    else if(state=="Minnesota"|state=="MN") "Midwest"
    else if(state=="Missouri"|state=="MO") "Midwest"
    else if(state=="Mississippi"|state=="MS") "South"
    else if(state=="Montana"|state=="MT") "West"
    else if(state=="North Carolina"|state=="NC") "South"
    else if(state=="North Dakota"|state=="ND") "Midwest"
    else if(state=="Nebraska"|state=="NE") "Midwest"
    else if(state=="New Hampshire"|state=="NH") "Northeast"
    else if(state=="New Jersey"|state=="NJ") "Northeast"
    else if(state=="New Mexico"|state=="NM") "West"
    else if(state=="Nevada"|state=="NV") "West"
    else if(state=="New York"|state=="NY") "Northeast"
    else if(state=="Ohio"|state=="OH") "Midwest"
    else if(state=="Oklahoma"|state=="OK") "South"
    else if(state=="Oregon"|state=="OR") "West"
    else if(state=="Pennsylvania"|state=="PA") "Northeast"
    else if(state=="Rhode Island"|state=="RI") "Northeast"
    else if(state=="South Carolina"|state=="SC") "South"
    else if(state=="South Dakota"|state=="SD") "Midwest"
    else if(state=="Tennessee"|state=="TN") "South"
    else if(state=="Texas"|state=="TX") "South"
    else if(state=="Utah"|state=="UT") "West"
    else if(state=="Virginia"|state=="VA") "South"
    else if(state=="Vermont"|state=="VT") "Northeast"
    else if(state=="Washington"|state=="WA") "West"
    else if(state=="Wisconsin"|state=="WI") "Midwest"
    else if(state=="West Virginia"|state=="WV") "South"
    else if(state=="Wyoming"|state=="WY") "West"
    else if(state=="American Samoa"|state=="AS") "Terr"
    else if(state=="Federated States of Micronesia"|state=="FM") "Terr"
    else if(state=="Guam"|state=="GU") "Terr"
    else if(state=="Marshall Islands"|state=="MH") "Terr"
    else if(state=="Northern Mariana Islands"|state=="MP") "Terr"
    else if(state=="Palau"|state=="PW") "Terr"
    else if(state=="Puerto Rico"|state=="PR") "Terr"
    else if(state=="Virgin Islands"|state=="VI") "Terr"
    else NA
}

findTZ <- function(state){
    if(is.na(state)) "EST"
    else if(state=="Alabama"|state=="AL") "CST"
    else if(state=="Alaska"|state=="AK") "PST"
    else if(state=="Arizona"|state=="AZ") "MST"
    else if(state=="Arkansas"|state=="AR") "CST"
    else if(state=="California"|state=="CA") "PST"
    else if(state=="Colorado"|state=="CO") "MST"
    else if(state=="Connecticut"|state=="CT") "EST"
    else if(state=="District of Columbia"|state=="DC") "EST"
    else if(state=="Delaware"|state=="DE") "EST"
    else if(state=="Florida"|state=="FL") "EST"
    else if(state=="Georgia"|state=="GA") "EST"
    else if(state=="Hawaii"|state=="HI") "PST"
    else if(state=="Idaho"|state=="ID") "MST"
    else if(state=="Illinois"|state=="IL") "CST"
    else if(state=="Indiana"|state=="IN") "CST"
    else if(state=="Iowa"|state=="IA") "CST"
    else if(state=="Kansas"|state=="KS") "CST"
    else if(state=="Kentucky"|state=="KY") "EST"
    else if(state=="Louisiana"|state=="LA") "CST"
    else if(state=="Maine"|state=="ME") "EST"
    else if(state=="Maryland"|state=="MD") "EST"
    else if(state=="Massachusetts"|state=="MA") "EST"
    else if(state=="Michigan"|state=="MI") "CST"
    else if(state=="Minnesota"|state=="MN") "CST"
    else if(state=="Mississippi"|state=="MS") "CST"
    else if(state=="Missouri"|state=="MO") "CST"
    else if(state=="Montana"|state=="MT") "MST"
    else if(state=="Nebraska"|state=="NE") "CST"
    else if(state=="Nevada"|state=="NV") "PST"
    else if(state=="New Hampshire"|state=="NH") "EST"
    else if(state=="New Jersey"|state=="NJ") "EST"
    else if(state=="New Mexico"|state=="NM") "MST"
    else if(state=="New York"|state=="NY") "EST"
    else if(state=="North Carolina"|state=="NC") "EST"
    else if(state=="North Dakota"|state=="ND") "MST"
    else if(state=="Ohio"|state=="OH") "EST"
    else if(state=="Oklahoma"|state=="OK") "CST"
    else if(state=="Oregon"|state=="OR") "PST"
    else if(state=="Pennsylvania"|state=="PA") "EST"
    else if(state=="Rhode Island"|state=="RI") "EST"
    else if(state=="South Carolina"|state=="SC") "EST"
    else if(state=="South Dakota"|state=="SD") "MST"
    else if(state=="Tennessee"|state=="TN") "EST"
    else if(state=="Texas"|state=="TX") "CST"
    else if(state=="Utah"|state=="UT") "MST"
    else if(state=="Vermont"|state=="VT") "EST"
    else if(state=="Virginia"|state=="VA") "EST"
    else if(state=="Washington"|state=="WA") "PST"
    else if(state=="West Virginia"|state=="WV") "EST"
    else if(state=="Wisconsin"|state=="WI") "CST"
    else if(state=="Wyoming"|state=="WY") "MST"
    else if(state=="American Samoa"|state=="AS") "PST"
    else if(state=="Federated States of Micronesia"|state=="FM") "PST"
    else if(state=="Guam"|state=="GU") "PST"
    else if(state=="Marshall Islands"|state=="MH") "PST"
    else if(state=="Northern Mariana Islands"|state=="MP") "PST"
    else if(state=="Palau"|state=="PW") "PST"
    else if(state=="Puerto Rico"|state=="PR") "EST"
    else if(state=="Virgin Islands"|state=="VI") "EST"
    else "EST"
}

codeLoc <- function(cntry,st){
    if(is.na(cntry)) NA
    else if((cntry== "United States" & !(is.na(st)))| cntry=="Puerto Rico"|cntry=="US Minor Outlying Islands"|
            cntry=="Virgin Islands (USA)"|cntry=="American Samoa"|
            cntry=="Guam"|cntry=="Northern Mariana Islands"|
            cntry=="Marshall Islands"|cntry=="Micronesia, Federal State of"|
            cntry=="Palau") 'US'    
    else "Global"
}

ageCat2 <- function(x){
    if(is.na(x)){
        cat <- NA
    }else{
        age <- year(today())-as.integer(x)
        if (age >= 18 & age <35) 'under35'
        else if(age >= 35 & age <50) 'age35to49'
        else if(age >= 50 & age <=90) 'fiftyAndUp'
        else NA
    }}

add_row_numbers <- function(df, name = "row_number", zero_based = FALSE) {
    # Drop variable if exists
    if (name %in% names(df)) df[, name] <- NULL
    # Create sequence of integers
    sequence <- seq.int(1, to = nrow(df))
    if (zero_based) sequence <- sequence - 1L
    # Add sequence to data frame
    df[, name] <- sequence
    # Move variable to the first column position
    df <- select(df, !!name, everything())
    return(df)
}

codePersonSamplingSizeCat <- function(sz,kind){
    if(is.na(sz)& is.na(kind)) NA
    else if(is.na(sz)& kind!="pub_ed") NA   
    else if(is.na(sz)& kind=="pub_ed") "pub_ed"
    else if(kind=="pub_ed") "pub_ed"
    else if(sz== "1-24") NA
    else if(sz=="25-49"|sz=="50-99") "XS"
    else if(sz=="100-249") "SM"
    else if(sz=="250-499"|sz=="500-999") "MD"
    else if(sz=="1000-2499"|sz=="2500-4999") "LG"
    else if(sz=="5000-9999"|sz=="10000-24999"|sz=="25000 and over") "XL"
    else NA}

sortMgmt <- function(jobTitle,bossTitle,numOverseen){
    mgmtTitles <- c("Partner, Principal","President, CEO, Chairman","CHRO, CHCO","VP or Asst/Assoc VP","Asst. or Assoc. Vice Pres","Director or Asst/Assoc Director",
                    "Supervisor")
    nonmgmtTitles <- c("Consultant","Coordinator","Legal Counsel","Representative, Associate","Specialist","Other","Administrative Assistant","Administrator")
    if(is.na(jobTitle)){
        outCat <- "Worker"
    }else if(jobTitle %in% mgmtTitles){
        outCat <- "Manager"
    }else if(jobTitle %in% nonmgmtTitles){
        outCat <- "Worker"
    }else if (is.na(bossTitle)|is.na(numOverseen)){
        outCat <- "Worker" 
    }else if(jobTitle == "Manager, Generalist" & (bossTitle=="Administrator"|bossTitle=="HR Manager"|numOverseen=="0")){
        outCat <- "Worker"
    }else if (jobTitle == "Manager, Generalist" & bossTitle!="Administrator"& bossTitle!="HR Manager"&numOverseen!="0"){
        outCat <- "Manager"
    }else {outCat <- "Worker"}
    return(outCat)
}

findGovEd <- function(orgType,indus,domain){
    if(is.na(orgType) & is.na(indus)){
        sector <- "Private"
    }else if(is.na(orgType) & (indus=="Education"|indus=="Government")){
        sector <- "pub_ed"
    }else if(is.na(orgType) & indus!="Education" & indus!="Government"){
        sector <- "Private"
    }else if(is.na(indus) & (orgType=="Govt Sector - Federal"|orgType=="Govt Sector - State/Local")){
        sector <- "pub_ed"
    }else if(is.na(indus) & orgType!="Govt Sector - Federal"& orgType!="Govt Sector - State/Local"){
        sector <- "Private"
    }else if(grepl(".gov",domain)==T){
        sector <- "pub_ed"
    }else if(orgType=="Govt Sector - Federal"|orgType=="Govt Sector - State/Local"|indus=="Education"|indus=="Government"){
        sector <- "pub_ed"
    }else {sector <- "Private"}
    return(sector)    
}

codeGender <- function(gen,pref){
    if(is.na(gen)&is.na(pref)){
        x<-NA
    }else if(is.na(gen)& (pref=='Miss'|pref=='Mrs.' | pref=='Ms.')){
        x<-"Female"
    }else if(is.na(gen)& pref=='Mr.'){
        x<-"Male"
    }else if(is.na(gen)& pref!='Mr.'& pref!='Miss'& pref!='Mrs.'& pref!='Ms.'){
        x<-NA
    }else if(gen=='Female'|gen=='Male'){
        x<-gen
    }else {x<-NA}
    return(x)
}

###############################################################################################################################################
# After loading functions, start here:                                                                                                        #
#      IF someone has pulled sample in the last 2-3 weeks, you can start with the cleaned memberlist from that point; JUMP TO LINE 410        #
#      ELSE:                                                                                                                                  #
#      Read in dataset (starting in August 2020, this comes from the Data Warehouse; to find it go to the #membership-counts Slack channel    #
#         and find #the most recent "SHRM Active Member Roster" link.                                                                         #
#      Save the new file to S:/Departments/Research & Insights/Sampling/Member Lists                                                          #
###############################################################################################################################################

newdat <- read_csv('./working/2021 P+S Democratization of Work (HR)_N33333_2021-03-19.csv') #n=302352
nrow(newdat)


#Who is a manager vs. a worker> To align with BLS, if they have a manager job title, Manager, otherwise worker. 
#Our category "Manager, Generalist" is ambiguous, so if they report to a manager or administrator, or have no direct reports we treat them as worker

newdat$level <- mapply(sortMgmt,newdat$Standard_Job_Title,newdat$Supervisor_Title,newdat$Employee_Oversee,SIMPLIFY = T)
newdat$level <- as.factor(newdat$level)
descr::freq(newdat$level)

projectName <- "All Active Roster - Edited"
projDir <- "./working/"

#write out one file with all sample information
newdat %>% write_csv(paste0(projDir,projectName,"_N",nrow(newdat),"_",lubridate::today(),".csv"))


#Note from Kerri: This variable changed from "Product_Name" to "membership_item". It also looks like some of the "products" were updated.
table(newdat$membership_item)
# 
# #We want to keep professional, corportate and global members, but drop student, retired, India
#Note from Kerri: I've updated this variable with the changes from DataWarehouse. However, I wasn't sure if we could include Executive Network members, so I've
#excluded them for now.
keepList <- c("Affinity Membership","Corporate Membership",
                "Corporate Membership-three month extention","Global Online Comp Membership - 1 Month",
                "Global Online Comp Membership - 3 Month","Global Online Comp Membership - 6 Month",
                "Global Online Membership","Global Online Membership - 2 Year",
                "Global Online Membership - 3 Year","Professional Comp Membership - 1 Month",
                "Professional Comp Membership - 3 Month","Professional Comp Membership - 6 Month",
                "Professional Membership","Professional Membership - 2 Year",
                "Professional Membership - 3 Year","Professional Membership - 6 Month",
                "SHRM Complimentary Membership - 1 year","SHRM Life Membership",
                "SHRM Life Membership Renewal") 

# #keep Professional, corporate (Note from Kerri: Excluding Executive Network level members for now until we get clarity on whether we can sample from them)
newdat <- newdat %>% filter(membership_item %in% keepList)
nrow(newdat) #N=275490
 
# # confirm this is current data; median value for Membership_Paid_Through should be at least 6 months from now
#Note from Kerri: Variable appears to not exist in the current roster. I tried using expiration_date instead. However, using this variable
# doesn't give us dates at least 6 months from now.
newdat$expiration_date <- as.Date(newdat$expiration_date, "%m/%d/%Y")
summary(newdat$expiration_date)


nrow(newdat)
colnames(newdat)


# ###########Deal with all duplicate and invalid records
# 
# #if people belong to multiple chapters, they have multiple records in this dataset that are otherwise identical

############################################
#Note from Kerri: This line no longer worked now that the variable names were changed. It looks like Liz is basically removing certain columns from the dataset
#to avoid keeping duplicates. I removed variables that appeared to be causing the issue of duplicates.
newdat <- newdat %>% select(-c(chapter_name:chapter_number,promo_code))




# 
# #remove duplicate records
newdat <- unique(newdat) #n=272568
nrow(newdat)
# 

# #check for records without an email address
#Note from Kerri: "Email" field was changed to lowercase in most recent dataset.
newdat$email <- tolower(newdat$email)
newdat %>% filter(is.na(email)) %>% nrow()
# 
# #drop 319 records with a dummy email address (no email provided to SHRM, dummy is generated for Single-Sign-On)
#Note from Kerri: "Email" field was changed to lowercase in most recent dataset.
rowsWithoutEmail <- grep("guest-[0-9]{8}@shrm.org",newdat$email)
newdat <- newdat[-rowsWithoutEmail,] #N=272249
rm(rowsWithoutEmail)
nrow(newdat)
# 
newdat<- add_row_numbers(newdat)
# 
# # # Duplicate emails to resolve--often this is easiest to do manually, as duplicate records are caused by
# #inconsistent stuff in the member data. If you have >100 duplicate emails at this point, there is probably a consistent
# #characteristic causing them, so look at the data, figure out what the issue is and write some code to resolve it.
# #Otherwise, look at the csv and create a list of rows to drop 
# #(Most common reason is a different Cert_End_Date; keep whichever row has the later cert end date) other reasons
# #can be incomplete contact information, two different cert dates
# #
# 
dupEmails <- pull(newdat[which(duplicated(newdat$email)),"email"])
newdat %>% filter(email %in% dupEmails) %>% arrange(email) %>% write_csv('temp9.csv')
# 
# #remove bad dup records
recsToDrop <- c(178191, 189798, 186462, 179239, 125260)

# 
newdat <- newdat %>% filter(!row_number %in% recsToDrop)
if(length(which(duplicated(newdat$email)))==0) "Continue" else "More duplicates to resolve"
nrow(newdat)
# #N=272244



# #remove 109 who have not do not want any communication (remove TRUE)
#Note from Kerri: "Disallow_All_Comm" changed to "disallow_all_communication"
newdat %>% filter(disallow_all_communication == T) %>% nrow()
newdat <- newdat %>% filter(disallow_all_communication == F)#N=272135
nrow(newdat)


# #Remove 538 SHRM employee/contractor emails
table(newdat$disallow_all_communication)
newdat$Email_Domain <- sapply(newdat$email, function(x) str_split(x,"@", 2)[[1]][2])
newdat %>% filter(Email_Domain=="shrm.org") %>% nrow()
newdat <- newdat %>% filter(is.na(Email_Domain) | Email_Domain!="shrm.org") #N=271597
nrow(newdat)


# #remove 47090 who have not do not want email communication (remove TRUE)
#Note from Kerri: "Disallow_Email_Comm" changed to "disallow_email_communication"
table(newdat$disallow_email_communication)
newdat %>% filter(disallow_email_communication == T) %>% nrow()
newdat <- newdat %>% filter(disallow_email_communication == F)#N=224507
nrow(newdat)



# #Change names to title case (do this before save because its very slow)
newdat$First_Name <- tools::toTitleCase(newdat$First_Name)
newdat$Last_Name <- tools::toTitleCase(newdat$Last_Name)
# 
saveRDS(newdat, paste0("./Member Lists/ActiveMembers_",today(),"_DupsandOptOutRemoved_Kerri.rdata"))#N=224507

#################################################################################################
newdat <- readRDS("./Member Lists/ActiveMembers_2021-04-12_DupsandOptOutRemoved_Derrick 4-12.rdata") #N=224507
nrow(newdat)

##CREATE VARIABLES FOR PERSON-LEVEL WEIGHTING SAMPLING

#Who is a manager vs. a worker> To align with BLS, if they have a manager job title, Manager, otherwise worker. 
#Our category "Manager, Generalist" is ambiguous, so if they report to a manager or administrator, or have no direct reports we treat them as worker

newdat$level <- mapply(sortMgmt,newdat$Standard_Job_Title,newdat$Supervisor_Title,newdat$Employee_Oversee,SIMPLIFY = T)
newdat$level <- as.factor(newdat$level)
descr::freq(newdat$level)

#Almost 25K people who declined to provide gender gave a title that is gender linked (mr/mrs/ms/miss), so use those fields together to label gender
newdat$gender <- mapply(codeGender,newdat$Gender,newdat$Name_Prefix,SIMPLIFY = T)
newdat$gender <- as.factor(newdat$gender)
newdat$gender <- fct_recode(newdat$gender,NULL = "Undisclosed")
descr::freq(newdat$gender)

#For education, need to collapse into the categories we use for weighting
newdat$education <- as.factor(newdat$Education)
newdat$education <- fct_recode(newdat$education,lessBach="High School / GED",lessBach="Associate's Degree",lessBach="Some College",lessBach="Not Identified",
                               bach="Bachelor's Degree",bach="Bachelor's Degree, HR",bach="Bachelor's Degree, non-HR",bach="College Beyond Bachelor",
                               mast="Doctorate",mast="JD",mast="Master's Degree",mast="Master's Degree, HR",mast="Master's Degree, non-HR",
                               mast="MBA",mast="MBA, HR Concentration",mast="MBA, non-HR Concentration")
newdat$education <- newdat$education %>% fct_drop() %>% fct_relevel("lessBach","bach","mast")
descr::freq(newdat$education)

#For age, start from birth year and calculate age into our weighting categories
newdat$age <- unlist(sapply(newdat$Birth_Year,ageCat2))
newdat$age <- ordered(newdat$age, levels =c('under35','age35to49','fissftyAndUp'))
descr::freq(newdat$age)

#Collapse ethnicity to weighting levels
newdat$ethnicity <- as.factor(newdat$Ethnicity)
newdat$ethnicity <- fct_recode(newdat$ethnicity,white="White",
                               black="Black/African American",
                               apa="Asian",apa="Asian/Pacific-Islander",apa="Native Hawaiian/Pacific Islander",
                               latino="Hispanic", latino="Hispanic/Other Latino",latino="Hispanic/White Latino",
                               others="American Indian/Alaskan Native",others="Multicultural/Other",others="Other",
                               NULL = "Undisclosed")
newdat$ethnicity <- newdat$ethnicity %>% fct_drop() %>% fct_relevel("white","black","apa","latino","others")
descr::freq(newdat$ethnicity)

#clean up states find regions and add in location variable for US/nonUS
newdat$state <-unlist(mapply(cleanState,newdat$Ship_Addr_Country_Desc,newdat$Ship_Addr_State))
newdat$location <- unlist(mapply(codeLoc, newdat$country_name,newdat$state))
newdat$location <- ordered(newdat$location, levels =c('US','Global'))
descr::freq(newdat$location)


newdat$region <- sapply(newdat$state,findRegion)
newdat$region <- as.factor(newdat$region)
newdat$region <- fct_recode(newdat$region,NULL = "Terr")
descr::freq(newdat$region)

#create org size categories for weighting scheme
newdat$orgCat <- mapply(findGovEd,newdat$Org_Type,newdat$Industry_Category,newdat$Email_Domain,SIMPLIFY = T)
descr::freq(newdat$orgCat)
newdat$company_size <- mapply(codePersonSamplingSizeCat,sz=newdat$Company_Size,kind=newdat$orgCat,SIMPLIFY = T)
newdat$company_size <- as.factor(newdat$company_size)
newdat$company_size <- newdat$company_size %>% fct_drop() %>% fct_relevel("pub_ed","XS","SM","MD","LG","XL")
descr::freq(newdat$company_size)



#add time zones for invites by time zone
newdat$tz <- sapply(newdat$state,findTZ)
descr::freq(newdat$tz)

######Remove people ineligible for this study

#Remove Academicians (almost always do this except for Market-Research-type/new product studies)
#Note from Kerri: Standard_Job_Title renamed job_title
newdat %>% filter(job_title=="Academician") %>% nrow() #N=1064
#note when using a filter with !=, you have to add the "or is.na" if you want to retain those the na cases in addition to the ones
#that have a value that follows the rule
newdat <- newdat%>% filter(job_title!="Academician"|is.na(job_title))

 #N=223443

nrow(newdat)


#Remove Consultants (This depends on the study, you can remove all consultants or use a more complex approach as commented out below)
#Note from Kerri: Standard_Job_Title renamed job_title
newdat %>% filter(job_title=="Consultant") %>% nrow() #7761
newdat <- newdat %>% filter(job_title!="Consultant"|is.na(job_title))
nrow(newdat) #N=215682


newdat_recruit <- newdat %>% filter(job_function=="Employment/Recruitment" | job_function=="Compensation" | job_function=="Training/Development")
nrow(newdat_recruit) #N=14484

newdat_other <- newdat %>% filter(job_function !="Employment/Recruitment" | job_function != "Compensation" | job_function !="Training/Development")
nrow(newdat_other)

nrow(newdat)


### CREATING OTHER ONLY POOL ###

#Remove those used for most recent surveys (it's your judgement call about how far back to go)
#In this case, I'll take out everyone already used in the last month 

samp4 <- read_csv("./2021 P+S Democratization of Work/2021 P+S Democratization of Work (HR)_N33333_2021-03-19.csv") %>% select(email=email)
samp5 <- read_csv("./2021 Business Travel Survey/2021 Business Travel Survey_N33333_2021-04-13.csv") %>% select(email=email)
samp6 <- read_csv("./2021 Empathy INdex Pilot Interest to Members/2021 Empathy Index Pilot Interest to Members_N4000_2021-03-24.csv") %>% select(email=email)
samp7 <- read_csv("./2021 Empathy INdex Pilot Interest to Members/SAMPLE B 2021 Empathy Index Pilot Interest to Members_N5000_2021-04-12.csv") %>% select(email=email)
samp8 <- read_csv("./2021 FFCRA Survey/2021 FFCRA Survey_N33547_2021-04-06.csv") %>% select(email=email)

#remove MR panel (not always necessary, but we've been going to them a lot, so pull them out now)
#mr <- read_csv('./Other Lists/MarketResearchPanelistsEmailOnly.csv')
#mr$email <- tolower(mr$email)
#mr <- mr %>% select(email)

#NOTE: I am keeping in the MR panel for Benchmarking study given their good RR.
used <- c(samp4$email, samp5$email, samp6$email, samp7$email, samp8$email)
length(which(duplicated(used)))
used <- unique(used) #95880 used
summary(used)
rm(samp4, samp5, samp6, samp7, samp8)

#remove the used people from the pool
pool_other <- newdat_other %>% filter(email %in% used==F) 

#if study is US only, remove global
pool_other <- pool_other %>% filter(country_code=="US") #N=71957
summary(pool_other)
nrow(pool_other)




#########################################################
#NOTE: Special filtering for FFCRA survey.
#pool2 <- pool %>% filter(job_function=="Benefits" | job_function=="Compensation" | job_function=="Employee Relations" | job_function=="HR Generalist" | job_function=="Legal")
#descr::freq(pool2$job_function)

#pool3 <- pool2 %>% filter(company_size=="100-249" | company_size=="24-Jan" | company_size=="25-49" | company_size=="250-499" | company_size=="50-99")
#descr::freq(pool3$company_size)

#nrow(pool3) #33547

#Sampling (use all)
#samp=pool3

#########################################################


#if you don't have any other requirements for the sample, pull a simple random sample
#if you are sampling from subsamples, use the appropriate mods to the code commented out below
#if you need full stratified sampling, scroll down to the block below
set.seed(4500)

respRate <- .03
targetComplete <- 900
sampSize <- round(if((targetComplete/respRate) < nrow(pool_other)) targetComplete/respRate else nrow(pool),0)
samp_other <- pool_other %>% sample_n(size=sampSize,replace = FALSE)
nrow(samp_other)

#adding in elibigle Recruitment people into the sample
samp <- merge.data.frame(samp_other, newdat_recruit, all=TRUE, no.dups = TRUE)
nrow(samp)

projectName <- "2021 Benchmarking Wave 1"
projDir <- "./2021 Benchmarking Wave 1/"

#write out one file with all sample information
samp %>% write_csv(paste0(projDir,projectName,"_N",nrow(samp),"_",lubridate::today(),".csv"))

#Note from Kerri: First_Name, Last_Name, Email variable names all changed from previous)
samp %>% select(firstname, lastname, email) %>%
    write_csv(paste0(projDir, projectName, "_N", nrow(samp), "_forQualtrics_", lubridate::today(),".csv"))

descr::freq(samp$tz)

#write out files with only information required for mailings 
samp %>% filter(tz=="EST") %>% select(firstname,lastname,email) %>% 
    write_csv(paste0(projDir,projectName,"EST_N","_",nrow(samp %>% filter(tz=="EST")),"forQualtrics_",lubridate::today(),".csv"))

samp %>% filter(tz=="CST") %>% select(firstname,lastname,email) %>% 
    write_csv(paste0(projDir,projectName,"CST_N","_",nrow(samp %>% filter(tz=="CST")),"forQualtrics_",lubridate::today(),".csv"))

samp %>% filter(tz=="MST") %>% select(firstname,lastname,email) %>%
    write_csv(paste0(projDir,projectName,"MST_N","_",nrow(samp %>% filter(tz=="MST")),"forQualtrics_",lubridate::today(),".csv"))

samp %>% filter(tz=="PST") %>% select(firstname,lastname,email) %>%
   write_csv(paste0(projDir,projectName,"PST_N","_",nrow(samp %>% filter(tz=="PST")),"forQualtrics_",lubridate::today(),".csv"))

##################################BEGIN STRATIFIED SAMPLING BLOCK#######################################################################################
#
# #############create tables for target samples
# #set up tables for population proportions for each demographic variable in individual weighting scheme
# levelTable <- data.frame(level=c("Manager","Worker"),grop=c(0.32,0.68),stringsAsFactors = F)
# genderTable <- data.frame(gender=c("Male","Female"),grop=c(0.29,0.71),stringsAsFactors = F)
# edTable <- data.frame(education=c("lessBach","bach","mast"),grop=c(0.38,0.43,0.19),stringsAsFactors = F)
# ageTable <- data.frame(age=c("under35","age35to49","fiftyAndUp"),grop=c(0.34,0.37,0.29),stringsAsFactors = F)
# raceTable <- data.frame(ethnicity=c("white","black","apa","latino","others"),grop=c(0.67,0.12,0.05,0.13,0.03),stringsAsFactors = F)
# regionTable <- data.frame(region=c("Northeast","Midwest","South","West"),grop=c(0.2,0.22,0.35,0.24),stringsAsFactors = F)
# company_sizeTable <- data.frame(company_size=c("pub_ed","XS","SM","MD","LG","XL"),grop=c(0.17,0.28,0.07,0.09,0.11,0.28),stringsAsFactors = F)
# 
# #function to combine two tables
# combineDataFrames<-function(t1,t2){
#     newDF <- data.frame(matrix(nrow=1,ncol=ncol(t1)+ncol(t2)-1))
#     colnames(newDF)<- c(colnames(t1)[1:ncol(t1)-1],colnames(t2)[1:ncol(t2)-1],"mProp")
#     newDF <- newDF[-1,]
#     outIndex=1
#     for (x in 1:nrow(t1)){
#         a <- as.character(t1[x,1:ncol(t1)-1])
#         c1 <- as.numeric(t1[x,ncol(t1)])
#         for(y in 1:nrow(t2)){
#             b <- as.character(t2[y,1:ncol(t2)-1])
#             c2 <- as.numeric(t2[y,ncol(t2)])
#             c <- c1*c2
#             newDF[outIndex,] <- c(a,b,c)
#             outIndex <- outIndex+1
#         }
#     }
#     return(newDF)
# }
# 
# #keep combining tables until you have included all of the variables that you want,e.g.
# # s1 <- combineDataFrames(levelTable,genderTable)
# # s2 <- combineDataFrames(s1,edTable)
# # s3 <- combineDataFrames(s2,ageTable)
# # s4 <- combineDataFrames(s3,raceTable)
# # s5 <- combineDataFrames(s4,regionTable)
# # s6 <- combineDataFrames(s5,company_sizeTable)
# # targetTable <- s6
# # rm(s1,s2,s3,s4,s5,s6)
# 
# step1 <- combineDataFrames(company_sizeTable,edTable)
# targetTable <- combineDataFrames(step1,levelTable)
# 
# #add target sample sizes to the table
# desiredSampleSize = 20000
# targetTable$desiredN <- sapply(targetTable$mProp, function(x) round(as.numeric(x)*desiredSampleSize,0))
# 
# #Functions to identify available sample, depending on number of variables in sampling design
# countAvail2Vars <- function(pool,targetTable){
#     pool %>% filter(!!sym(colnames(targetTable)[1])==targetTable[p,1] &
#                                  !!sym(colnames(targetTable)[2])==targetTable[p,2]) %>% 
#     nrow()}
# 
# countAvail3Vars <- function(pool,targetTable){
#     x<- pool %>% filter(!!sym(colnames(targetTable)[1])==targetTable[p,1] &
#                                  !!sym(colnames(targetTable)[2])==targetTable[p,2] &
#                                  !!sym(colnames(targetTable)[3])==targetTable[p,3])%>% 
#                  nrow()}
# 
# countAvail4Vars <- function(pool,targetTable){
#     pool %>% filter(!!sym(colnames(targetTable)[1])==targetTable[p,1] &
#                                  !!sym(colnames(targetTable)[2])==targetTable[p,2] &
#                                  !!sym(colnames(targetTable)[3])==targetTable[p,3] &
#                                  !!sym(colnames(targetTable)[4])==targetTable[p,4])%>% 
#                  nrow()}
# countAvail5Vars <- function(pool,targetTable){
#     pool %>% filter(!!sym(colnames(targetTable)[1])==targetTable[p,1] &
#                                  !!sym(colnames(targetTable)[2])==targetTable[p,2] &
#                                  !!sym(colnames(targetTable)[3])==targetTable[p,3] &
#                                  !!sym(colnames(targetTable)[4])==targetTable[p,4] &
#                                  !!sym(colnames(targetTable)[5])==targetTable[p,5])%>% 
#                  nrow()}
# 
# countAvail6Vars <- function(pool,targetTable){
#     pool %>% filter(!!sym(colnames(targetTable)[1])==targetTable[p,1] &
#                                  !!sym(colnames(targetTable)[2])==targetTable[p,2] &
#                                  !!sym(colnames(targetTable)[3])==targetTable[p,3] &
#                                  !!sym(colnames(targetTable)[4])==targetTable[p,4] &
#                                  !!sym(colnames(targetTable)[5])==targetTable[p,5] &
#                                  !!sym(colnames(targetTable)[6])==targetTable[p,6])%>% 
#                  nrow()}
# 
# countAvail7Vars <- function(pool,targetTable){
#     pool %>% filter(!!sym(colnames(targetTable)[1])==targetTable[p,1] &
#                                  !!sym(colnames(targetTable)[2])==targetTable[p,2] &
#                                  !!sym(colnames(targetTable)[3])==targetTable[p,3] &
#                                  !!sym(colnames(targetTable)[4])==targetTable[p,4] &
#                                  !!sym(colnames(targetTable)[5])==targetTable[p,5] &
#                                  !!sym(colnames(targetTable)[6])==targetTable[p,6] &
#                                  !!sym(colnames(targetTable)[7])==targetTable[p,7])%>% 
#                  nrow()}
# 
# 
# #add available sample sizes to the table
# avail <- list()
# for(p in 1:nrow(targetTable)){
#     avail <- c(avail,countAvail3Vars(pool,targetTable))
# }
# targetTable$available<-as.numeric(avail)
# targetTable$feasibility <- mapply(function(x,y)if(x>y)"Not Enough in pool to meet target" else "-",targetTable$desiredN,targetTable$available)
# 
# targetTable
# 
# #Before you go on, look at the target table. If you have feasibility for enough variables, go on. Otherwise, go back and remove stratifying variables.
# #You can also collapse some variables, but you'll need to recode factors of the variable you want to use and make new tables 
# #Functions to sample from appropriately subset data, depending on number of variables in sampling design
# 
# sample2Vars <- function(pool,targetTable){
#     sample_n(pool %>% filter(!!sym(colnames(targetTable)[1])==targetTable[p,1] &
#                                  !!sym(colnames(targetTable)[2])==targetTable[p,2]),
#              min(targetTable$desiredN[p],targetTable$available[p]),replace=F)}
# 
# sample3Vars <- function(pool,targetTable){
#     sample_n(pool %>% filter(!!sym(colnames(targetTable)[1])==targetTable[p,1] &
#                                  !!sym(colnames(targetTable)[2])==targetTable[p,2] &
#                                  !!sym(colnames(targetTable)[3])==targetTable[p,3]),
#              min(targetTable$desiredN[p],targetTable$available[p]),replace=F)}
# 
# sample4Vars <- function(pool,targetTable){
#     sample_n(pool %>% filter(!!sym(colnames(targetTable)[1])==targetTable[p,1] &
#                                  !!sym(colnames(targetTable)[2])==targetTable[p,2] &
#                                  !!sym(colnames(targetTable)[3])==targetTable[p,3] &
#                                  !!sym(colnames(targetTable)[4])==targetTable[p,4]),
#              min(targetTable$desiredN[p],targetTable$available[p]),replace=F)}
# 
# sample5Vars <- function(pool,targetTable){
#     sample_n(pool %>% filter(!!sym(colnames(targetTable)[1])==targetTable[p,1] &
#                                  !!sym(colnames(targetTable)[2])==targetTable[p,2] &
#                                  !!sym(colnames(targetTable)[3])==targetTable[p,3] &
#                                  !!sym(colnames(targetTable)[4])==targetTable[p,4] &
#                                  !!sym(colnames(targetTable)[5])==targetTable[p,5]),
#              min(targetTable$desiredN[p],targetTable$available[p]),replace=F)}
# 
# sample6Vars <- function(pool,targetTable){
#     sample_n(pool %>% filter(!!sym(colnames(targetTable)[1])==targetTable[p,1] &
#                                  !!sym(colnames(targetTable)[2])==targetTable[p,2] &
#                                  !!sym(colnames(targetTable)[3])==targetTable[p,3] &
#                                  !!sym(colnames(targetTable)[4])==targetTable[p,4] &
#                                  !!sym(colnames(targetTable)[5])==targetTable[p,5] &
#                                  !!sym(colnames(targetTable)[6])==targetTable[p,6]),
#              min(targetTable$desiredN[p],targetTable$available[p]),replace=F)}
# 
# sample7Vars <- function(pool,targetTable){
#     sample_n(pool %>% filter(!!sym(colnames(targetTable)[1])==targetTable[p,1] &
#                                  !!sym(colnames(targetTable)[2])==targetTable[p,2] &
#                                  !!sym(colnames(targetTable)[3])==targetTable[p,3] &
#                                  !!sym(colnames(targetTable)[4])==targetTable[p,4] &
#                                  !!sym(colnames(targetTable)[5])==targetTable[p,5] &
#                                  !!sym(colnames(targetTable)[6])==targetTable[p,6] &
#                                  !!sym(colnames(targetTable)[7])==targetTable[p,7]),
#              min(targetTable$desiredN[p],targetTable$available[p]),replace=F)}
# 
# #actually create the sample, employing functions above
# set.seed(2342)
# variablesSampled <- ncol(targetTable-4)
# stratSample <- pool[0,]
# 
# if(variablesSampled==2){
#     for(p in 1:nrow(targetTable)){stratSample <- rbind.data.frame(stratSample,sample2Vars(pool,targetTable))}
# }else if(variablesSampled==3){
#     for(p in 1:nrow(targetTable)){stratSample <- rbind.data.frame(stratSample,sample3Vars(pool,targetTable))}
# }else if(variablesSampled==4){
#     for(p in 1:nrow(targetTable)){stratSample <- rbind.data.frame(stratSample,sample3Vars(pool,targetTable))}
# }else if(variablesSampled==5){
#     for(p in 1:nrow(targetTable)){stratSample <- rbind.data.frame(stratSample,sample3Vars(pool,targetTable))}
# }else if(variablesSampled==6){
#     for(p in 1:nrow(targetTable)){stratSample <- rbind.data.frame(stratSample,sample3Vars(pool,targetTable))}
# }else if(variablesSampled==7){
#     for(p in 1:nrow(targetTable)){stratSample <- rbind.data.frame(stratSample,sample3Vars(pool,targetTable))}
# }else {print("You need to write a sampling function for a larger number of variables")}
# 
# #Check for any duplicates (this is just a sanity check that strata are distinct)
# which(duplicated(stratSample$Email))

# projectName <- "CostofRI"
# targetTable %>% write_csv(paste0("TargetTableFor",projectName,"_",lubridate::today(),".csv"))
# stratSample %>% write_csv(paste0("stratSampleFor",projectName,"_N",nrow(stratSample),"_",lubridate::today(),".csv"))
# stratSample %>% select(First_Name,Last_Name,Email) %>% write_csv(paste0("stratSampleFor",projectName,"_N",nrow(stratSample),"forQualtrics_",lubridate::today(),".csv"))
##################################END STRATIFIED SAMPLING BLOCK#######################################################################################


 }else {print("You need to write a sampling function for a larger number of variables")}
# 
# #Check for any duplicates (this is just a sanity check that strata are distinct)
# which(duplicated(stratSample$Email))

# projectName <- "CostofRI"
# targetTable %>% write_csv(paste0("TargetTableFor",projectName,"_",lubridate::today(),".csv"))
# stratSample %>% write_csv(paste0("stratSampleFor",projectName,"_N",nrow(stratSample),"_",lubridate::today(),".csv"))
# stratSample %>% select(First_Name,Last_Name,Email) %>% write_csv(paste0("stratSampleFor",projectName,"_N",nrow(stratSample),"forQualtrics_",lubridate::today(),".csv"))
##################################END STRATIFIED SAMPLING BLOCK#######################################################################################


