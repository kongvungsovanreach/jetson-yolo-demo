#import required modules

class LockIt():
    def __init__(self, callback, args = [], password = None):
        self._callback = callback
        self._args = args
        self._password = password
    
    #unlock the code
    def unlock(self, password):
        if password:
            if password == self._password:
                args_len = len(self._args)
                if args_len == 0:
                    self._callback()
                elif args_len == 1:
                    self._callback(self._args[0])
                elif args_len == 2:
                    self._callback(self._args[0], self._args[1])
                elif args_len == 3:
                    self._callback(self._args[0], self._args[1], self._args[2])
            else:
                print('password is incorrect.')