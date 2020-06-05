import time;

i = 20;
while(i > 0):
    i = i - 1;
    print("Doing some work and sleeping for 1 second");
    time.sleep(1);

print("I am done, Bye");

f = open("/log/1.log", "a")
f.write("Now the file has more content!")
f.close()
