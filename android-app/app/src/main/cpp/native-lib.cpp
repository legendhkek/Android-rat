#include <jni.h>
#include <string>
#include <unistd.h>
#include <sys/ptrace.h>
#include <pthread.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/prctl.h>
#include <sys/mman.h>
#include <dlfcn.h>
#include <dirent.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

// Anti-debugging techniques at native level for FUD
static bool debugger_detected = false;

// Check for TracerPid in /proc/self/status
bool check_tracer_pid() {
    const char* status_path = "/proc/self/status";
    FILE* fp = fopen(status_path, "r");
    if (fp == nullptr) return false;
    
    char line[256];
    while (fgets(line, sizeof(line), fp)) {
        if (strncmp(line, "TracerPid:", 10) == 0) {
            int pid;
            sscanf(line, "TracerPid: %d", &pid);
            fclose(fp);
            return pid != 0;
        }
    }
    fclose(fp);
    return false;
}

// Anti-debugging using ptrace
bool anti_ptrace() {
    return ptrace(PTRACE_TRACEME, 0, 1, 0) < 0;
}

// Check for debugging ports
bool check_debug_ports() {
    int ports[] = {23946, 5555, 5037, 8000};
    for (int port : ports) {
        struct sockaddr_in addr;
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock < 0) continue;
        
        addr.sin_family = AF_INET;
        addr.sin_port = htons(port);
        addr.sin_addr.s_addr = inet_addr("127.0.0.1");
        
        if (connect(sock, (struct sockaddr*)&addr, sizeof(addr)) == 0) {
            close(sock);
            return true;
        }
        close(sock);
    }
    return false;
}

// Continuous anti-debugging thread
void* anti_debug_thread(void* arg) {
    while (true) {
        if (check_tracer_pid() || anti_ptrace() || check_debug_ports()) {
            debugger_detected = true;
            // Kill process if debugger detected
            _exit(0);
        }
        usleep(1000000); // Check every second
    }
    return nullptr;
}

// String obfuscation using XOR
std::string deobfuscate(const char* data, int length, char key) {
    std::string result;
    for (int i = 0; i < length; i++) {
        result += (char)(data[i] ^ key);
    }
    return result;
}

// Initialize native anti-detection
extern "C" JNIEXPORT void JNICALL
Java_com_apkmodifier_AntiDetection_nativeInit(JNIEnv* env, jobject /* this */) {
    // Start anti-debugging thread
    pthread_t thread;
    pthread_create(&thread, nullptr, anti_debug_thread, nullptr);
    pthread_detach(thread);
}

// Check if debugger is present
extern "C" JNIEXPORT jboolean JNICALL
Java_com_apkmodifier_AntiDetection_nativeAntiDebug(JNIEnv* env, jobject /* this */) {
    return debugger_detected || check_tracer_pid() || anti_ptrace();
}

// Hide from process list
extern "C" JNIEXPORT void JNICALL
Java_com_apkmodifier_AntiDetection_hideProcess(JNIEnv* env, jobject /* this */) {
    // Rename process to look like system service
    const char* fake_name = "system_server";
    prctl(PR_SET_NAME, fake_name, 0, 0, 0);
}

// Memory protection
extern "C" JNIEXPORT void JNICALL
Java_com_apkmodifier_AntiDetection_protectMemoryNative(JNIEnv* env, jobject /* this */) {
    // Make memory pages non-readable to prevent dumping
    void* addr = (void*)0x10000;
    size_t length = 0x1000;
    mprotect(addr, length, PROT_NONE);
}

// Detect emulator at native level
extern "C" JNIEXPORT jboolean JNICALL
Java_com_apkmodifier_AntiDetection_isEmulatorNative(JNIEnv* env, jobject /* this */) {
    // Check for emulator files
    const char* emulator_files[] = {
        "/dev/socket/qemud",
        "/dev/qemu_pipe",
        "/system/lib/libc_malloc_debug_qemu.so",
        "/sys/qemu_trace",
        "/system/bin/qemu-props"
    };
    
    for (const char* file : emulator_files) {
        if (access(file, F_OK) == 0) {
            return true;
        }
    }
    
    // Check CPU features
    FILE* fp = fopen("/proc/cpuinfo", "r");
    if (fp) {
        char line[256];
        while (fgets(line, sizeof(line), fp)) {
            if (strstr(line, "goldfish") || strstr(line, "ranchu")) {
                fclose(fp);
                return true;
            }
        }
        fclose(fp);
    }
    
    return false;
}

// Encrypt string at native level
extern "C" JNIEXPORT jstring JNICALL
Java_com_apkmodifier_AntiDetection_nativeEncrypt(
    JNIEnv* env, jobject /* this */, jstring data, jstring key) {
    
    const char* data_str = env->GetStringUTFChars(data, nullptr);
    const char* key_str = env->GetStringUTFChars(key, nullptr);
    
    std::string encrypted;
    int key_len = strlen(key_str);
    int data_len = strlen(data_str);
    
    for (int i = 0; i < data_len; i++) {
        encrypted += (char)(data_str[i] ^ key_str[i % key_len]);
    }
    
    env->ReleaseStringUTFChars(data, data_str);
    env->ReleaseStringUTFChars(key, key_str);
    
    return env->NewStringUTF(encrypted.c_str());
}

// Check for Frida
extern "C" JNIEXPORT jboolean JNICALL
Java_com_apkmodifier_AntiDetection_detectFrida(JNIEnv* env, jobject /* this */) {
    // Check for Frida libraries
    void* handle = dlopen("libfrida-agent.so", RTLD_NOW);
    if (handle) {
        dlclose(handle);
        return true;
    }
    
    // Check for Frida threads
    DIR* dir = opendir("/proc/self/task");
    if (dir) {
        struct dirent* entry;
        while ((entry = readdir(dir)) != nullptr) {
            if (entry->d_type == DT_DIR) {
                char path[256];
                snprintf(path, sizeof(path), "/proc/self/task/%s/comm", entry->d_name);
                FILE* fp = fopen(path, "r");
                if (fp) {
                    char comm[256];
                    if (fgets(comm, sizeof(comm), fp)) {
                        if (strstr(comm, "frida") || strstr(comm, "gum-js-loop")) {
                            fclose(fp);
                            closedir(dir);
                            return true;
                        }
                    }
                    fclose(fp);
                }
            }
        }
        closedir(dir);
    }
    
    return false;
}
