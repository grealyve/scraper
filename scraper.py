import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

class Scrape: 
    dataList = []
    websites = {
        "databases":"https://breached.vc/Forum-Databases",
        "stealerlogs": "https://breached.vc/Forum-Stealer-Logs"}

    #Scrapes the data and puts in a list then inserts the list into a list.
    def getData(self, source, driver):
        try:
            td = driver.find_elements(By.CSS_SELECTOR, ".inline_row")
            for element in td:
                tempList = []
                tempList.append(element.find_element(By.CSS_SELECTOR, ".subject_new").text)  #topic
                tempList.append(element.find_element(By.CSS_SELECTOR, ".author.smalltext").text[3:-2]) #author
                tempList.append(element.find_element(By.CSS_SELECTOR, ".forum-display__thread-date").text) #date of topic created
                tempList.append(source)
                self.dataList.append(tempList)
        except(Exception) as error:
            print("Data couldn't be scraped please consider the CSS changes",error)

    #Reaches the websites in order to get data.
    def insertData(self):
        try:
            driver = webdriver.Firefox(executable_path="geckodriver") #You may have to give path of the webdriver!
            for website in self.websites:
                if(website == "databases"):
                    url = self.websites[website]
                    driver.get(url)
                    time.sleep(3)
                    self.getData(website, driver)
                    time.sleep(3)
                    
                elif(website == "stealerlogs"):
                    url = self.websites[website]
                    driver.get(url)
                    time.sleep(3)
                    self.getData(website, driver)
                    time.sleep(2)

            driver.close()
        except(Exception) as error:
            print("Couldn't reach the website or there is another issue",error)

    #Creates very first dataframe
    def createTable(self):
        pd.DataFrame(self.dataList, columns=["Topic", "Author", "Date", "Source"]).to_csv('data.csv', index=False)
        self.dataList = []

    #Checks if the data already inserted or not so that we get a unique dataframe.
    def uniqueTable(self):
        df = pd.read_csv("data.csv", encoding="UTF-8")
        self.insertData()
        df2 = pd.DataFrame(self.dataList, columns=["Topic", "Author", "Date", "Source"])

        topic_list = df2["Topic"].tolist()
        topic_list2 = df["Topic"].tolist()
        author_list = df2["Author"].tolist()
        date_list = df2["Date"].tolist()
        source_list = df2["Source"].tolist()

        for new_topic in topic_list:
            if new_topic not in topic_list2:
                index = topic_list.index(new_topic)
                topic = (topic_list[index])
                author =(author_list[index])
                date = (date_list[index])
                source = (source_list[index])
                new_row = {"Topic":topic, "Author": author, "Date": date, "Source": source}
                df = df.append(new_row, ignore_index=True)
                print(topic,author,date,source)
            else:
                continue

        df.to_csv('data.csv', index=False)
        self.dataList = []
        df2 = df2.iloc[0:0]
        df = df.iloc[0:0]

if __name__ == "__main__":
    scraper = Scrape()
    #Creates data.csv file and inserts the first dataframe.
    try:
        scraper.insertData()
        fileName = "data.csv"
        filepath = os.getcwd()
        path = os.path.join(filepath,fileName)
        with open(path, "w") as csvFile:
            print("CSV file has been created.")
        scraper.createTable()
    except(Exception, FileExistsError) as error:
        print("Unexpected error :", error)

    while True:
        scraper.uniqueTable()
        curr_time = time.strftime("%H:%M:%S", time.localtime())
        print("Data has been inserted at :", curr_time)
        time.sleep(3600)