import pandas as pd
import argparse
import socket
import re
import geocoder


def get_input():
    """
    Get input parameters
    :return: input parameters
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-file", help="file path",action="store")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

    args = parser.parse_args()
    return args


def check_MBI(mbi):
    """
    :param mbi: mbi as in csv
    :return: checks if the given string is an MBI - 11 characters, A-Z and 0-9, exculding 'BILOSZ'.
    """
    mbi = mbi.replace("-","")
    pattern = re.compile("[A-Z0-9]+")
    if pattern.fullmatch(mbi) is not None and len(mbi)==11:
        chars = set('BILOSZ')
        if not(any((c in chars) for c in mbi)):
            return mbi
    return 0


def check_credit_card_num(cc_num):
    """
    :param cc_num: cc_num as in csv
    :return: checks if the given string is a credit card - 11-19 characters, 0-9.
             looks for the issuer by the first digit.
    """
    cc_num = cc_num.replace("-", "").replace("_", "").replace(" ", "")
    issued_by = 0
    if cc_num.isnumeric() and 13 <= len(cc_num) <= 19:
        first_dig = cc_num[0]
        if first_dig == "3":
            issued_by = "Amex/Diners/CarteBlanche"
        elif first_dig == "4":
            issued_by = "Visa"
        elif first_dig == "5":
            issued_by = "MasterCard"
        elif first_dig == "6":
            issued_by = "Discover"
        elif first_dig == "9":
            issued_by = "Airline"
        return cc_num, issued_by
    return 0, 0


def check_phone_num(phone):
    """
    :param phone: phone as in csv
    :return: checks if the given string is a phone number - 10-14 characters, 0-9.
    """
    phone = phone.replace("-", "").replace("+", "").replace("_", "").replace(" ", "")
    if phone.isnumeric() and 10 <= len(phone) <= 14:
        return phone
    return 0


def convert_to_df(file):
    """
    Cleaning csv file and extracting info.
    :return: df of financial data
    """
    financials_df = pd.read_csv(file, engine='python', index_col=False)
    med_ids, cc_nums, issuers, phone_nums = [], [], [], []
    found_cc, found_mbi, found_phone = "",  "", ""
    for index, row in financials_df.iterrows():
        cc_number, issuer = check_credit_card_num(row['cc_num'])
        p_num = check_phone_num(row['phone_num'])
        med_ids.append(check_MBI(row['medicare_id']))
        cc_nums.append(cc_number)
        issuers.append(issuer)
        phone_nums.append(p_num)
        if cc_number: found_cc = "Credit Cards, "
        if check_MBI(row['medicare_id']): found_mbi = "Medicare Beneficiary Identifiers, "
        if p_num: found_phone = "Phone Numbers"
    financials_df['medicare_id'] = med_ids
    financials_df['cc_num'] = cc_nums
    financials_df['issuer'] = issuers
    financials_df['phone_num'] = phone_nums

    print(f"Found the following sensitive value types: {found_cc}{found_mbi}{found_phone}")
    return financials_df


if __name__ == '__main__':
    inputs = get_input()
    file_path = str(inputs.file)
    verbose = inputs.verbose
    financials_df = convert_to_df(file_path)

    if verbose: print(f"Found {financials_df.shape[0]} records in the given csv")
    financials_df.to_csv('arranged_financial_data.csv', index=False)
