import struct

class MPS7():
    
    def __init__(self, binary_file):
        with open(binary_file, 'rb') as f:        
            self.binary_data = f.read()
        
        self.records = self.decode_binary()


    def decode_binary(self):
        """
        Covert the MPS7 binary data into a list of tuples
        
        See format characters in pydocs here:
        https://docs.python.org/3.1/library/struct.html#format-characters
        
        Header:
        | 4 byte magic string "MPS7" | 1 byte version | 4 byte (uint32) # of records |
        
        Record:
        | 1 byte record type enum | 4 byte (uint32) Unix timestamp | 8 byte (uint64) user ID |

        """
        header = struct.unpack_from('!4cBi', self.binary_data, 0)
        records = []
        header_size = 9
        offset=header_size
        base_record_offset = 13
        deb_cred_offset = 8
        i=0
        num_records = header[5]
        
        while i < num_records:
            i+=1
            record = struct.unpack_from('!BLQ', self.binary_data, offset)
            _type = record[0]
            
            #this is a debit or credit and has an additional value
            if _type in [0,1]:
                record = struct.unpack_from('!BLQd', self.binary_data, offset)
                offset+=base_record_offset+deb_cred_offset
            else:
                offset+=base_record_offset
            
            records.append(record)
        
        return records


    def get_records(self, _id):
        return [
            record for record in self.records
            if _id == record[2]
        ]


    def sum_debits_credits(self, records):
        """add credits and subtract debits"""
        total = 0
        for record in records:
            if record[0] == 0:
                total -= record[3]
            elif record[0] == 1:
                total += record[3]
        return total


    def sum_record_types(self):
        """
        Return a list of record type totals ordered by their
        respective binary enum types.  
        Record type enum:
        
        * 0x00: Debit
        * 0x01: Credit
        * 0x02: StartAutopay
        * 0x03: EndAutopay
        
        """
        results = [0,0,0,0]
        
        for record in self.records:
            if record[0] in [0,1]:
                results[record[0]] += record[3]
            else:
                results[record[0]] += 1
        
        return results


if __name__ == '__main__':
    mps7 = MPS7('txnlog.dat')
    totals = mps7.sum_record_types()
    print('what is the total amount in dollars of debits?')
    print(totals[0])
    print('What is the total amount in dollars of credits?')
    print(totals[1])
    print('How many autopays were started?')
    print(totals[2])    
    print('How many autopays were ended?')
    print(totals[3])
    print('What is balance of user ID 2456938384156277127?')
    print(mps7.sum_debits_credits(mps7.get_records(2456938384156277127)))
