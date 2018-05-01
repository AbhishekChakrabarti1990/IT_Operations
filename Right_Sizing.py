"""
Created on Fri Apr 27 08:08:42 2018

@author: AbhishekChakrabarti1990

This script will accept a csv ticket dump (without headers) in the following format:
    TicketID,Priority,SubmitDate
Submit date should be in the format M(M)/D(D)/YYYY H(H):MI

Sample CSV format:
INC1,Medium,4/26/2018 10:28
INC2,High,4/25/2018 17:16
INC3,Medium,4/25/2018 16:05
INC4,Medium,4/25/2018 11:11

Also, it requires the following input:
    Number of months for which ticket dump is present
    SLA/MTTR in hours. If MTTRs are less than SLAs, provide the MTTR values
"""

class Tickets:
    TicketID = [];
    Priority = 1;
    Shift = 1;

    
parser_total = [];
TicketDump = [];


CritNum = 0;
CritNumS1 = 0;
CritNumS2 = 0;
CritNumS3 = 0;

HighNum = 0;
HighNumS1 = 0;
HighNumS2 = 0;
HighNumS3 = 0;

MedNum = 0;
MedNumS1 = 0;
MedNumS2 = 0;
MedNumS3 = 0;

LowNum = 0;
LowNumS1 = 0;
LowNumS2 = 0;
LowNumS3 = 0;

FTE = 0;
FTES1 = 0;
FTES2 = 0;
FTES3 = 0;
   
FileName = input("Please enter the filename of the ticket dump. File should be present in the same folder as this script\n");

with open(FileName,'r') as reader:
    for line in reader:
        parser_total.append(line);

NumMonth = int(input("Please enter number of months covered by ticket dump\n"));
SCrit = int(input("Please enter the SLA/MTTR (in hours) for Critical priority requests\n"));
SHigh = int(input("Please enter the SLA/MTTR (in hours) for High priority requests\n"));
SMed = int(input("Please enter the SLA/MTTR (in hours) for Medium priority requests\n"));
SLow = int(input("Please enter the SLA/MTTR (in hours) for Low priority requests\n"));

print("We have considered below shift timings as per standard 24/7 models\n");
print("Shift 1 is from 06:00 to 14:00\n");
print("Shift 2 is from 15:00 to 23:00\n");
print("Shift 3 is from 00:00 to 05:00\n");



for i in parser_total:
    ticketholder = Tickets();
    holder = i.split(',');
    ticketholder.TicketID = holder[0];
    
    if holder[1] == "Critical":
        ticketholder.Priority = 1;
    elif holder[1] == "High":
        ticketholder.Priority = 2;
    elif holder[1] == "Medium":
        ticketholder.Priority = 3;
    elif holder[1] == "Low":
        ticketholder.Priority = 4;
    else:
        ticketholder.Priority = 0;
    
    holder = holder[2].split();
    holder = holder[1].split(':');
    holder = int(holder[0]);
    
    if holder in range(0,6):
        ticketholder.Shift = 3;
    elif holder in range(6,15):
        ticketholder.Shift = 1;
    elif holder in range(15,24):
        ticketholder.Shift = 2;
    else:
        ticketholder.Shift = 0;
    TicketDump.append(ticketholder);
    

for i in TicketDump:
    if i.Priority == 1:
        CritNum+= 1;
    elif i.Priority == 2:
        HighNum+= 1;
    elif i.Priority == 3:
        MedNum+= 1;
    elif i.Priority == 4:
        LowNum+= 1;
    else:
        print("Priority is ",i.Priority, " and Shift is ",i.Shift);
       

for i in TicketDump:    
    if i.Priority == 1 and i.Shift == 1:
        CritNumS1+= 1;
    elif i.Priority == 1 and i.Shift == 2:
        CritNumS2+= 1;
    elif i.Priority == 1 and i.Shift == 3:
        CritNumS3+= 1;
    
        
    elif i.Priority == 2 and i.Shift == 1:
        HighNumS1+= 1;
    elif i.Priority == 2 and i.Shift == 2:
        HighNumS2+= 1;
    elif i.Priority == 2 and i.Shift == 3:
        HighNumS3+= 1;
    
    elif i.Priority == 3 and i.Shift == 1:
        MedNumS1+= 1;
    elif i.Priority == 3 and i.Shift == 2:
        MedNumS2+= 1;
    elif i.Priority == 3 and i.Shift == 3:
        MedNumS3+= 1;
    
    elif i.Priority == 4 and i.Shift == 1:
        LowNumS1+= 1;
    elif i.Priority == 4 and i.Shift == 2:
        LowNumS2+= 1;
    elif i.Priority == 4 and i.Shift == 3:
        LowNumS3+= 1;
        
    else:
        print("Ticket ID is ",i.TicketID, ", Priority is ",i.Priority, " and Shift is ",i.Shift);

FTE = int(((CritNum*SCrit)+(HighNum*SHigh)+(MedNum*SMed)+(LowNum*SLow))/(NumMonth*8*30));
FTES1 = int(((CritNumS1+HighNumS1+MedNumS1+LowNumS1)*FTE)/(CritNum+HighNum+MedNum+LowNum));
FTES2 = int(((CritNumS2+HighNumS2+MedNumS2+LowNumS2)*FTE)/(CritNum+HighNum+MedNum+LowNum));
FTES3 = FTE-(FTES1+FTES2);

print("You need ",FTE, " resource(s) to run operations\n");
print("You need ",FTES1," resource(s) in S1\n");
print("You need ",FTES2," resource(s) in S2\n");
print("You need ",FTES3," resource(s) in S3\n");