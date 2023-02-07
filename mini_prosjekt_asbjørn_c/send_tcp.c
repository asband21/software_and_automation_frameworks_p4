#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define BUFSIZE 1024

int main(int argc, char *argv[])
{
    int sockfd, n;
    struct sockaddr_in serv_addr;
    char buffer[BUFSIZE];
    char *message = "jeg er en fisk";

    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        perror("Error: opening socket");
        exit(1);
    }

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    serv_addr.sin_port = htons(8007);

    if (connect(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0)
    {
        perror("Error: connecting");
        exit(1);
    }

    n = write(sockfd, message, strlen(message));
    if (n < 0)
    {
        perror("Error: writing to socket");
        exit(1);
    }

    memset(buffer, 0, BUFSIZE);
    n = read(sockfd, buffer, BUFSIZE - 1);
    if (n < 0)
    {
        perror("Error: reading from socket");
        exit(1);
    }
    printf("Received message: %s\n", buffer);

    close(sockfd);
    return 0;
}
