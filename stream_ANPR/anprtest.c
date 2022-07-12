#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>
int main(void){
	
	sleep(5);
	system("python3 fbanpr.py plate_h.xml");

    return 0;
}
