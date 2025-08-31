#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_INPUT 1024

// Function to convert Markdown to HTML
void convert_markdown_to_html(const char *markdown, char *html) {
    char temp[MAX_INPUT];
    strcpy(temp, markdown);
    
    // Convert headers
    if (temp[0] == '#') {
        int level = 0;
        while (temp[level] == '#') {
            level++;
        }
        
        if (level <= 6) {
            sprintf(html, "<h%d>%s</h%d>", level, temp + level + 1, level);
            return;
        }
    }
    
    // Convert bold text
    char *bold_start = strstr(temp, "**");
    if (bold_start) {
        char *bold_end = strstr(bold_start + 2, "**");
        if (bold_end) {
            *bold_start = '\0';
            *bold_end = '\0';
            sprintf(html, "%s<strong>%s</strong>%s", temp, bold_start + 2, bold_end + 2);
            return;
        }
    }
    
    // Convert italic text
    char *italic_start = strstr(temp, "*");
    if (italic_start && italic_start[1] != '*' && italic_start != temp) {
        char *italic_end = strstr(italic_start + 1, "*");
        if (italic_end) {
            *italic_start = '\0';
            *italic_end = '\0';
            sprintf(html, "%s<em>%s</em>%s", temp, italic_start + 1, italic_end + 1);
            return;
        }
    }
    
    // Convert code
    char *code_start = strstr(temp, "`");
    if (code_start) {
        char *code_end = strstr(code_start + 1, "`");
        if (code_end) {
            *code_start = '\0';
            *code_end = '\0';
            sprintf(html, "%s<code>%s</code>%s", temp, code_start + 1, code_end + 1);
            return;
        }
    }
    
    // Convert links
    char *link_start = strstr(temp, "[");
    if (link_start) {
        char *link_mid = strstr(link_start, "](");
        char *link_end = strstr(link_start, ")");
        if (link_mid && link_end && link_mid < link_end) {
            *link_start = '\0';
            *link_mid = '\0';
            *link_end = '\0';
            sprintf(html, "%s<a href=\"%s\">%s</a>%s", 
                   temp, link_mid + 2, link_start + 1, link_end + 1);
            return;
        }
    }
    
    // Convert images
    char *img_start = strstr(temp, "![");
    if (img_start) {
        char *img_mid = strstr(img_start, "](");
        char *img_end = strstr(img_start, ")");
        if (img_mid && img_end && img_mid < img_end) {
            *img_start = '\0';
            *img_mid = '\0';
            *img_end = '\0';
            sprintf(html, "%s<img src=\"%s\" alt=\"%s\">%s", 
                   temp, img_mid + 2, img_start + 2, img_end + 1);
            return;
        }
    }
    
    // Default: wrap in paragraph tags
    sprintf(html, "<p>%s</p>", temp);
}

int main() {
    char markdown[MAX_INPUT];
    char html[MAX_INPUT * 2]; // HTML can be longer than markdown
    
    printf("=== Markdown to HTML Converter ===\n");
    printf("Enter 'exit' to quit the converter.\n\n");
    
    while (1) {
        printf("Markdown: ");
        if (fgets(markdown, MAX_INPUT, stdin) == NULL) {
            break;
        }
        
        // Remove newline character
        markdown[strcspn(markdown, "\n")] = 0;
        
        // Check for exit command
        if (strcmp(markdown, "exit") == 0) {
            printf("Goodbye! Happy converting!\n");
            break;
        }
        
        // Convert and display
        convert_markdown_to_html(markdown, html);
        printf("HTML: %s\n\n", html);
    }
    
    return 0;
}
