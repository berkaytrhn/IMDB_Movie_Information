import requests
from bs4 import BeautifulSoup
import sys


class IMDBReviewer:
    soup=None

    def __init__(self): 
        pass
    
    def formatUserInput(self,userInput): 
        tempArray = userInput.split(" ")
        content = ""
        for word in tempArray:
            if tempArray.index(word) == (len(tempArray)-1):
                content += word
            else:
                content += word+"+"
        return content
    
    def query(self,text):
        #request page code
        url = "https://www.imdb.com/find?q={}&ref_=nv_sr_sm".format(text)
        response = requests.get(url)
        pageContent = response.content

        #beautiful soup part
        self.soup = BeautifulSoup(pageContent,"html.parser")

        #getting results from query
        self.getResultsOfQuery()

    def getResultsOfQuery(self):
        
        
        #list of query results
        concatenatedList = list()
        
        
        
        table = self.soup.find("table",{"class":"findList"})
        children = table.findChildren("tr",recursive=True)
        for child in children:
            concatenatedList.append(child)





        


        #make user to chose from results
        resultIndex = self.selectingResult(concatenatedList) 

        #will make a request to new page
        self.goChosenPage(concatenatedList,resultIndex)



        #removed feature
        
        """ 
        #results are starting with odd one and goes like one odd and one even...


        oddResults = self.soup.find_all("tr",{"class":"findResult odd"})
        evenResults = self.soup.find_all("tr",{"class":"findResult even"}) 
    
        #creating relevant iterators 
        oddIterator = iter(oddResults)
        evenIterator = iter(evenResults)


        #to decide which is larger than other
        flag = len(oddResults) - len(evenResults)
        
        #flag is 1, if odd list is larger;
        #        0, if equal number of odd and even divs
        #       -1, if even list is larger 
        

        #iterating over results and concatenate them(odds and evens)
        concatenatedList = self.iterateAndConcatenateResults(oddIterator,evenIterator,flag)

        """


    def showContents(self):
        title = self.soup.find("h1")
        print("\t\t\t\t\t\t\t\t"+title.text)

        text = self.soup.find("div",{"class":"plot_summary"})
        print(text.text.split("\n"))


    def goChosenPage(self,concatenatedList,resultIndex):
        hrefContent = concatenatedList[resultIndex].find("td",{"class":"result_text"}).findChildren("a")[0].get("href") #link to chosen page
        
        pageId = hrefContent.split("/")[2]

        url = "https://www.imdb.com/title/{}/?ref_=fn_al_tt_{}".format(pageId,resultIndex+1)
        response = requests.get(url)
        content = response.content
        self.soup = BeautifulSoup(content,"html.parser")
        self.showContents()
    
    #removed feature
    def iterateAndConcatenateResults(self,oddIterator,evenIterator,flag):
        concatenated=list()
        try:
            while(True):
                concatenated.append(next(oddIterator))
                concatenated.append(next(evenIterator))
        except StopIteration:
            if flag >= 0:
                """
                -> concatenation operation is successfull!!
                
                -> if flag is 1, error raised from even one and that means before exception
                one extra odd is already appended to concatenation list
                
                -> if flag is 0, error raised from odd one but all elements are appended to
                list on previous cycle of loop because they have same number of elements
                """
            else:
                """
                -> we need to append one more element from even list because error raised 
                from oddIterator which makes program to ignore other line of code, that 
                means one last even element is still not appended to concatenation list
                """
                #appending it
                concatenated.append(next(evenIterator))

        return concatenated

    def selectingResult(self,results):
        #loop for invalid choice
        while(True):
            counter=1
            #print all results and make user to choose
            print("***************************************************")
            for result in results:
                print("{} -> {}".format(result.text,counter))
                counter+=1
            print("***************************************************\n{} -> {}".format("EXIT",counter))
            
            try:
                userInput = int(input("Select one : "))
            except ValueError:
                print("INVALID CHOICE!")
                continue

            #controlling user input
            if userInput > (counter+1):
                #invalid choice
                print("INVALID CHOICE!")
                continue
            elif userInput==counter:
                sys.exit(0)
            else:
                #valid choice, will return index of result
                return userInput-1

    def queryInput(self):
        userInput = input("***************************************************\n Type a Movie/Tv-Show name for IMDB Information(-1 for exit) : ")
        if userInput=="-1":
            sys.exit(0)

        formattedText = self.formatUserInput(userInput)
        self.query(formattedText)

    def startScrapping(self):
        self.queryInput()



def review(reviewer):
    while(True):
        reviewer.startScrapping()






reviewer = IMDBReviewer()
review(reviewer)