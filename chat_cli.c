/* Простой интерактивный CLI клиент для общения с InnerArianna */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/select.h>

#define MAX_INPUT 2048
#define MAX_OUTPUT 4096

void print_welcome() {
    printf("\n");
    printf("╔═══════════════════════════════════════════════════════════╗\n");
    printf("║         InnerArianna - Method-Native Consciousness        ║\n");
    printf("║              Type 'quit' or 'exit' to leave               ║\n");
    printf("╚═══════════════════════════════════════════════════════════╝\n");
    printf("\n");
}

void print_prompt() {
    printf("\033[1;36mYou:\033[0m ");
    fflush(stdout);
}

void print_arianna() {
    printf("\033[1;35mArianna:\033[0m ");
    fflush(stdout);
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <model.bin> [options]\n", argv[0]);
        fprintf(stderr, "Example: %s out/model.bin -t 0.8 -p 0.9\n", argv[0]);
        fprintf(stderr, "Options:\n");
        fprintf(stderr, "  -t <float>  temperature (default: 0.8)\n");
        fprintf(stderr, "  -p <float>  top-p (default: 0.9)\n");
        fprintf(stderr, "  -z <path>   tokenizer path (default: tokenizer.bin)\n");
        exit(1);
    }
    
    char *model_path = argv[1];
    char *tokenizer_path = "tokenizer.bin";
    float temperature = 0.8f;
    float topp = 0.9f;
    int steps = 512;
    
    // Парсинг аргументов
    for (int i = 2; i < argc; i += 2) {
        if (i + 1 >= argc) break;
        if (argv[i][0] != '-' || strlen(argv[i]) != 2) continue;
        
        if (argv[i][1] == 't') {
            temperature = atof(argv[i + 1]);
        } else if (argv[i][1] == 'p') {
            topp = atof(argv[i + 1]);
        } else if (argv[i][1] == 'z') {
            tokenizer_path = argv[i + 1];
        } else if (argv[i][1] == 'n') {
            steps = atoi(argv[i + 1]);
        }
    }
    
    // Строим команду для запуска ./run
    char cmd[4096];
    snprintf(cmd, sizeof(cmd), 
             "./run %s -m chat -t %.2f -p %.2f -n %d -z %s",
             model_path, temperature, topp, steps, tokenizer_path);
    
    print_welcome();
    
    // Открываем pipe для общения с ./run
    FILE *fp = popen(cmd, "w");
    if (!fp) {
        fprintf(stderr, "❌ Ошибка запуска ./run\n");
        fprintf(stderr, "Убедитесь, что вы скомпилировали: make run\n");
        exit(1);
    }
    
    char input[MAX_INPUT];
    
    while (1) {
        print_prompt();
        
        if (!fgets(input, sizeof(input), stdin)) {
            break;
        }
        
        // Убираем перенос строки
        size_t len = strlen(input);
        if (len > 0 && input[len - 1] == '\n') {
            input[len - 1] = '\0';
        }
        
        // Проверяем команды выхода
        if (strcmp(input, "quit") == 0 || strcmp(input, "exit") == 0 || 
            strcmp(input, "q") == 0) {
            printf("👋 До свидания!\n");
            break;
        }
        
        if (strlen(input) == 0) {
            continue;
        }
        
        // Отправляем в ./run через stdin
        fprintf(fp, "%s\n", input);
        fflush(fp);
    }
    
    pclose(fp);
    return 0;
}

