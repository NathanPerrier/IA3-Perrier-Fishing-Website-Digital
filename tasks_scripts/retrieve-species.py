import os, sys

def main(argv):
        
    try:
        print('running')
        print(' EXEC -> ' + os.path.basename(__file__)) 

        # Unix ErrCode
        exit(0)

    except Exception as e:

        print( 'Err: ' + str( e ) )
        exit(1)

if __name__ == '__main__':
    main(sys.argv)
