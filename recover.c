
#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>

bool isJPEG(unsigned char *input) {
  if (input[0] == 0xff && input[1] == 0xd8 && input[2] == 0xff && (input[3] & 0xf0) == 0xe0) {
      return true;
  }    
  else {
      return false;
  }
}

int main(int argc, char *argv[]) {
    
    if (argc != 2) {
        return 1;
    }
    
    char *infile = argv[1];
    FILE *rawData = fopen(infile, "r");
    if (rawData == NULL) {
        fprintf(stderr, "What the heck, that's not raw data!\n");
        return 1;
    }
    
    unsigned char *buffer = malloc(512 * sizeof(char));
    char *filename = malloc(8 * sizeof(char));
    int blockLen = fread(buffer, 1, 512, rawData);
    int num = 0;
    
    
    while (blockLen == 512) {
        
        if (isJPEG(buffer)) {
            
            // create and open sequentially named jpeg file, writing first block
            sprintf(filename, "%03i.jpg", num);
            FILE *img = fopen(filename, "w");
            fwrite(buffer,512,1, img);
            blockLen = fread(buffer, 1, 512, rawData);
            
            // write 512 bytes of data unless another jpeg or eof is found
            while (!isJPEG(buffer) && blockLen == 512) {
                fwrite(buffer,512,1, img);    
                blockLen = fread(buffer, 1, 512, rawData);
            }
            
            num++;
            fclose(img);
        }
        
        blockLen = fread(buffer, 1, 512, rawData);
        
    }
    
    free(filename);
    free(buffer);
    fclose(rawData);
}