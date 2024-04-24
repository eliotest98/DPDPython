from Core.Executor import execute_test

if __name__ == "__main__":
    import sys

    print("Folder of test: " + sys.argv[0])
    execute_test(test_name=sys.argv[1], debug_active=sys.argv[2])
