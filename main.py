import csv
from datetime import datetime

# Initialize a dictionary to keep track of all transaction data, each key value will be a customerID.
record = {}

# Open the CSV file and read in the rows
with open('input.csv', 'r') as f:
  reader = csv.reader(f)

  # Iterate through the rows of the CSV file
  for row in reader:

    # check if the row is a valid transaction
    if len(row) < 3:
        continue
    if not row[0] or not row[1] or not row[2]:
        continue

    # Parse the row data and add it to our dictionary
    # Save transaction data in an array by month/year for each customerID
    date = datetime.strptime(row[1], "%m/%d/%Y")
    strdate = str(date.month) + '/' + str(date.year)
    if row[0] not in record:
        record[row[0]] = {}
    if strdate not in record[row[0]]:
        record[row[0]][strdate] = []
    record[row[0]][strdate].append([date.day, int(row[2])])

# Create and open the output file in write mode
with open('output.csv', 'w', newline='') as csvfile:

  # Create a csv writer object
  writer = csv.writer(csvfile)

  # We need to analyze each month for each customer where transaction data is given and write a row to the output.csv file containing the necessary data.
  for customerID in record:
    for strdate in sorted(record[customerID]):
        
        curdata = record[customerID][strdate]

        # Sort the transaction data for the month in increasing order by day
        curdata.sort(key=lambda x: x[0])

        curbalance = 0
        maxbalance = float('-inf')
        minbalance = float('inf')
        index = 0
        dayqueue = []
        curday = curdata[0][0]

        while index < len(curdata):
            if curdata[index][0] != curday:
                # Once we have all the transactions made in a day, apply credits then debits and update the min, max, and current balances.
                for val in dayqueue:
                    curbalance += val
                    maxbalance = max(maxbalance, curbalance)
                    minbalance = min(minbalance, curbalance)

                # Reset dayqueue and curday
                curday = curdata[index][0]
                dayqueue = [curdata[index][1]]
            else:
                # Put credits first and debits last in the dayqueue for the customer for easier analysis
                if curdata[index][1] < 0:
                    dayqueue.append(curdata[index][1])
                else:
                    dayqueue.insert(0, curdata[index][1])
            index += 1

        # Perform transaction analysis for the last day
        for val in dayqueue:
            curbalance += val
            maxbalance = max(maxbalance, curbalance)
            minbalance = min(minbalance, curbalance)

        # Write the data row to the output csv
        writer.writerow([customerID, strdate, str(minbalance), str(maxbalance), str(curbalance)])
