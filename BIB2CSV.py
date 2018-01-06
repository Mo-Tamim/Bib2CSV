
import json
import csv
import os



class BIB2CSV:
    def __init__(self, CSVName, BIBName,JsonName):
        self.CSVName = CSVName
        self.BIBName = BIBName
        self.JsoName = JsonName
        self.BIBData = {}

    def make_dict(self):
        with open(self.BIBName, 'r', encoding="utf8") as BIBFilePointer:
            line1 = ''
            longline = False
            for line in BIBFilePointer:
                line = line.strip()
                if '@' not in line and not line.endswith('},') and not line.endswith('},}'):
                    line1 += line
                    longline = True
                    continue
                if longline:
                    longline = False
                    line = line1 + line
                    line1 = ''
                if line.startswith('@'):
                    EntryKey = line[line.index('{') + 1:]
                    EntryKey = EntryKey.replace(',', '')
                    self.BIBData[EntryKey] = {}
                else:
                    name = line[:line.index('=')]
                    value = line[line.index('=') + 2:line.index('}')]
                    self.BIBData[EntryKey][name] = value
        # Save it to json file for future use
        with open(self.JsoName, 'w') as jo:
            json.dump(self.BIBData, jo, indent=2)

    def CreateCSV(self):
        # pdb.set_trace()

        BIBKeys = [Key for Key in self.BIBData]
        CSVHeader = ["ItemKey"]
        for HeaderItem in self.BIBData[BIBKeys[1]]:
            CSVHeader.append(HeaderItem)


        with open('CSVTemp.csv', 'w', encoding='utf-8', newline='') as CSVFilePointer:
            CSVWriterPointer = csv.writer(CSVFilePointer)
            for BibKey in self.BIBData:
                CSVLineContent = []
                # This loop take an item from the CSV and put its value in the CSV line
                for HeaderItem in CSVHeader:
                    if HeaderItem == "ItemKey":
                        CSVLineContent.append(BibKey)
                        continue
                    if HeaderItem in self.BIBData[BibKey]:
                        CSVLineContent.append(self.BIBData[BibKey][HeaderItem])
                    else:
                        CSVLineContent.append('')

                # This loop search for a new head item an add it to the CSV head
                for HeaderItem in self.BIBData[BibKey]:
                    if HeaderItem not in CSVHeader:
                        CSVHeader.append(HeaderItem)
                        CSVLineContent.append(self.BIBData[BibKey][HeaderItem])

                CSVWriterPointer.writerow(CSVLineContent)

        # print(CSVFilePointer.closed)

        with open('CSVTemp.csv') as CSVFilePointer:
            CSVReaderPointer = csv.reader(CSVFilePointer)
            with open(self.CSVName, 'w+', newline='') as CSVFilePointer2:
                CSVWriterPointer = csv.writer(CSVFilePointer2)
                CSVWriterPointer.writerow(CSVHeader)
                for Row in CSVReaderPointer:
                    CSVWriterPointer.writerow(Row)
        os.remove('CSVTemp.csv')



def main():
    CSVName ='CSVFile.csv'
    BIBName = 'ConferencePublications.bib'
    JsonName = 'JsonFile.json'
    BibConverter = BIB2CSV(CSVName, BIBName, JsonName)
    BibConverter.make_dict()
    BibConverter.CreateCSV()


if __name__ == '__main__':
    main()