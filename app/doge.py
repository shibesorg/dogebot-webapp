import dogecoinrpc


class DogeConnection():
    def __init__(self, username, password, host, port):
        self.username = username
        self.password = password
        self.host = host
        self.port = port

        try:
            self.conn = dogecoinrpc.connect_to_remote(
                self.username,
                self.password,
                host=self.host,
                port=self.port
            )
        except:
            # Add connection exception
            print('could not connect to the node.')

    # def get_keypair(self):
    #     public_key = self.conn.getnewaddress()
    #     priv_key = self.conn.dumpprivkey(public_key)
    #     return {'priv_key': priv_key, 'public_key': public_key}

    def get_balance(self, account_name):
        return self.conn.getbalance(account_name, minconf=1)

    def get_newaddress(self, account_name):
        return self.conn.getnewaddress(account_name)

    def send_from(self, from_account, to_address, amount, comment='Sent from shibes.org'):
        return self.conn.sendfrom(
            from_account,
            to_address,
            amount,
            minconf=1,
            comment=comment,
            comment_to=comment,
        )
