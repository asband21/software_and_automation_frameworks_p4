#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define BUFSIZE 1024

void error(char *msg)
{
    perror(msg);
    exit(1);
}

int main(int argc, char *argv[])
{
    int sockfd, newsockfd, portno;
    socklen_t clilen;
    char buffer[BUFSIZE];
    struct sockaddr_in serv_addr, cli_addr;
    int n;

    if (argc < 2)
    {
        fprintf(stderr, "Error: no port provided\n");
        exit(1);
    }

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0)
        error("Error: opening socket");

    memset(&serv_addr, 0, sizeof(serv_addr));
    portno = atoi(argv[1]);
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(portno);

    if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0)
        error("Error: binding");

    listen(sockfd, 5);
    clilen = sizeof(cli_addr);
    newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
    if (newsockfd < 0)
        error("Error: accepting");

    memset(buffer, 0, BUFSIZE);
    n = read(newsockfd, buffer, BUFSIZE - 1);
    if (n < 0)
        error("Error: reading from socket");

    printf("Received message: %s\n", buffer);

    n = write(newsockfd, "I received your message!", 22);
    if (n < 0)
        error("Error: writing to socket");

    close(newsockfd);
    close(sockfd);
    return 0;
}
