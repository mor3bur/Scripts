Data Researcher Home Assignment:
How to run:
python identify_sensitive_value_types.py -file file_path [-v]
example:  python identify_sensitive_value_types.py -file financials.csv 

return: Sensitive value types found in the csv file

Answers to questions:
1) What problems did you encounter when working with the data, if any?
Answer: I tried to extract the country mobile prefix from the phone number, but I had multiple countries for some of the code numbers so I did'nt do that.
Also, I needed to understand the format of an MBI and the length of a credit card number so I looked for that online.
2) In the provided file, there is a Street Address column. How would you approach
identifying this data?
Answer: I would try to extract the house number by looking for 0-9 characters, than I would extract the following letters as the street name. If the is a ',' then the following letters would probabaly be the street name. 


 
