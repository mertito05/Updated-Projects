#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_URL_LENGTH 2048
#define MAX_RESPONSE_SIZE 65536
#define MAX_LINKS 1000

typedef struct {
    char url[MAX_URL_LENGTH];
    char title[256];
    char content[1024];
} WebPage;

typedef struct {
    char links[MAX_LINKS][MAX_URL_LENGTH];
    int count;
} LinkList;

// Basic HTTP client simulation
void http_get(const char* url, char* response, int max_size) {
    // Simulate HTTP GET request
    printf("Fetching: %s\n", url);
    
    // Simulate different responses based on URL
    if (strstr(url, "example.com")) {
        snprintf(response, max_size,
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
            "<!DOCTYPE html>"
            "<html>"
            "<head><title>Example Domain</title></head>"
            "<body>"
            "<h1>Example Domain</h1>"
            "<p>This domain is for use in illustrative examples in documents.</p>"
            "<a href=\"/page1\">Page 1</a>"
            "<a href=\"/page2\">Page 2</a>"
            "<a href=\"https://www.iana.org/domains/example\">More information...</a>"
            "</body>"
            "</html>"
        );
    } else if (strstr(url, "page1")) {
        snprintf(response, max_size,
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
            "<!DOCTYPE html>"
            "<html>"
            "<head><title>Page 1</title></head>"
            "<body>"
            "<h1>Page 1 Content</h1>"
            "<p>This is the content of page 1.</p>"
            "<a href=\"/\">Home</a>"
            "</body>"
            "</html>"
        );
    } else {
        snprintf(response, max_size,
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
            "<!DOCTYPE html>"
            "<html>"
            "<head><title>404 Not Found</title></head>"
            "<body>"
            "<h1>404 Not Found</h1>"
            "<p>The requested URL was not found on this server.</p>"
            "</body>"
            "</html>"
        );
    }
}

// Extract HTML content from HTTP response
char* extract_html_content(const char* response) {
    char* html_start = strstr(response, "\r\n\r\n");
    if (html_start) {
        return html_start + 4; // Skip the HTTP headers
    }
    return (char*)response; // Return original if no headers found
}

// Basic HTML parsing to extract links
void extract_links(const char* html, LinkList* link_list) {
    const char* ptr = html;
    link_list->count = 0;
    
    while (*ptr && link_list->count < MAX_LINKS) {
        // Look for <a href="...">
        ptr = strstr(ptr, "href=\"");
        if (!ptr) break;
        
        ptr += 6; // Skip "href=\""
        
        // Find the end of the URL
        const char* end = strchr(ptr, '"');
        if (!end) break;
        
        // Extract the URL
        int url_length = end - ptr;
        if (url_length > 0 && url_length < MAX_URL_LENGTH - 1) {
            strncpy(link_list->links[link_list->count], ptr, url_length);
            link_list->links[link_list->count][url_length] = '\0';
            link_list->count++;
        }
        
        ptr = end + 1;
    }
}

// Extract text content from HTML (very basic)
void extract_text_content(const char* html, char* text, int max_size) {
    const char* ptr = html;
    char* text_ptr = text;
    int in_tag = 0;
    int text_length = 0;
    
    while (*ptr && text_length < max_size - 1) {
        if (*ptr == '<') {
            in_tag = 1;
        } else if (*ptr == '>') {
            in_tag = 0;
            // Add space after tags for readability
            if (text_length < max_size - 1) {
                *text_ptr++ = ' ';
                text_length++;
            }
        } else if (!in_tag && !isspace(*ptr)) {
            *text_ptr++ = *ptr;
            text_length++;
        } else if (!in_tag && isspace(*ptr) && text_length > 0 && 
                  text_ptr[-1] != ' ') {
            // Add single space between words
            *text_ptr++ = ' ';
            text_length++;
        }
        ptr++;
    }
    
    *text_ptr = '\0';
    
    // Trim trailing spaces
    while (text_length > 0 && isspace(text[text_length - 1])) {
        text[text_length - 1] = '\0';
        text_length--;
    }
}

// Normalize URL (very basic)
void normalize_url(const char* base_url, const char* relative_url, char* result) {
    if (strstr(relative_url, "http://") || strstr(relative_url, "https://")) {
        // Absolute URL
        strncpy(result, relative_url, MAX_URL_LENGTH - 1);
    } else if (relative_url[0] == '/') {
        // Root-relative URL
        const char* domain_start = strstr(base_url, "://");
        if (domain_start) {
            domain_start += 3;
            const char* path_start = strchr(domain_start, '/');
            if (path_start) {
                strncpy(result, base_url, path_start - base_url);
                strncat(result, relative_url, MAX_URL_LENGTH - strlen(result) - 1);
            } else {
                strncpy(result, base_url, MAX_URL_LENGTH - 1);
                strncat(result, relative_url, MAX_URL_LENGTH - strlen(result) - 1);
            }
        } else {
            strncpy(result, relative_url, MAX_URL_LENGTH - 1);
        }
    } else {
        // Relative URL
        // For simplicity, just append to base URL
        strncpy(result, base_url, MAX_URL_LENGTH - 1);
        // Remove filename part if exists
        char* last_slash = strrchr(result, '/');
        if (last_slash) {
            *(last_slash + 1) = '\0';
        }
        strncat(result, relative_url, MAX_URL_LENGTH - strlen(result) - 1);
    }
}

// Process a web page
void process_page(const char* url, WebPage* page) {
    char response[MAX_RESPONSE_SIZE];
    char html_content[MAX_RESPONSE_SIZE];
    
    // Fetch the page
    http_get(url, response, sizeof(response));
    
    // Extract HTML content
    char* html = extract_html_content(response);
    strncpy(html_content, html, sizeof(html_content) - 1);
    html_content[sizeof(html_content) - 1] = '\0';
    
    // Extract title (very basic)
    const char* title_start = strstr(html_content, "<title>");
    if (title_start) {
        title_start += 7;
        const char* title_end = strstr(title_start, "</title>");
        if (title_end) {
            int title_len = title_end - title_start;
            if (title_len > 255) title_len = 255;
            strncpy(page->title, title_start, title_len);
            page->title[title_len] = '\0';
        }
    }
    
    // Extract text content
    extract_text_content(html_content, page->content, sizeof(page->content));
    
    // Store URL
    strncpy(page->url, url, sizeof(page->url) - 1);
    page->url[sizeof(page->url) - 1] = '\0';
}

// Display page information
void display_page(const WebPage* page) {
    printf("\n=== Page Information ===\n");
    printf("URL: %s\n", page->url);
    printf("Title: %s\n", page->title);
    printf("Content: %s\n", page->content);
    printf("=========================\n");
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        printf("Usage: %s <URL>\n", argv[0]);
        printf("Example: %s http://example.com\n", argv[0]);
        return 1;
    }
    
    const char* start_url = argv[1];
    WebPage page;
    LinkList links;
    
    printf("Web Scraper Starting...\n");
    printf("Target URL: %s\n", start_url);
    
    // Process the starting page
    process_page(start_url, &page);
    display_page(&page);
    
    // Extract links from the page
    char response[MAX_RESPONSE_SIZE];
    http_get(start_url, response, sizeof(response));
    char* html = extract_html_content(response);
    extract_links(html, &links);
    
    printf("\nFound %d links:\n", links.count);
    for (int i = 0; i < links.count && i < 10; i++) {
        char normalized_url[MAX_URL_LENGTH];
        normalize_url(start_url, links.links[i], normalized_url);
        printf("%d. %s -> %s\n", i + 1, links.links[i], normalized_url);
    }
    
    if (links.count > 10) {
        printf("... and %d more links\n", links.count - 10);
    }
    
    printf("\nWeb scraping completed successfully!\n");
    
    return 0;
}
