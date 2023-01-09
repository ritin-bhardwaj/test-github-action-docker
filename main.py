import os

def main():
    input = os.environ["NAME"]
    print(input)
    my_input = os.environ["IAP_TOKEN"]
    print(my_input)
    my_output = f"Hello {my_input}"

    print(f"::set-output name=myOutput::{my_output}")
    #print(myOutput=my_output" >> $GITHUB_OUTPUT)

if __name__ == "__main__":
    main()