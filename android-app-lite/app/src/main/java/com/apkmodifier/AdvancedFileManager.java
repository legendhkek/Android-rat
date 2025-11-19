package com.apkmodifier;

import android.content.Context;
import android.os.Environment;
import android.util.Log;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;
import java.util.zip.ZipOutputStream;
import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Advanced File Manager for bot file operations
 * Handles file listing, searching, uploading, downloading, compression
 */
public class AdvancedFileManager {
    private static final String TAG = "FileManager";
    private Context context;
    
    public AdvancedFileManager(Context context) {
        this.context = context;
    }
    
    /**
     * List all files in a directory recursively
     */
    public JSONArray listFiles(String path, boolean recursive) {
        JSONArray files = new JSONArray();
        try {
            File directory = new File(path);
            if (!directory.exists() || !directory.isDirectory()) {
                return files;
            }
            
            File[] fileList = directory.listFiles();
            if (fileList != null) {
                for (File file : fileList) {
                    try {
                        JSONObject fileInfo = new JSONObject();
                        fileInfo.put("name", file.getName());
                        fileInfo.put("path", file.getAbsolutePath());
                        fileInfo.put("size", file.length());
                        fileInfo.put("is_directory", file.isDirectory());
                        fileInfo.put("last_modified", file.lastModified());
                        fileInfo.put("readable", file.canRead());
                        fileInfo.put("writable", file.canWrite());
                        fileInfo.put("hidden", file.isHidden());
                        
                        files.put(fileInfo);
                        
                        if (recursive && file.isDirectory()) {
                            JSONArray subFiles = listFiles(file.getAbsolutePath(), true);
                            for (int i = 0; i < subFiles.length(); i++) {
                                files.put(subFiles.get(i));
                            }
                        }
                    } catch (Exception e) {
                        Log.e(TAG, "Error processing file: " + file.getName(), e);
                    }
                }
            }
        } catch (Exception e) {
            Log.e(TAG, "Error listing files", e);
        }
        return files;
    }
    
    /**
     * Search for files by name pattern
     */
    public JSONArray searchFiles(String rootPath, String pattern) {
        JSONArray results = new JSONArray();
        try {
            searchFilesRecursive(new File(rootPath), pattern.toLowerCase(), results);
        } catch (Exception e) {
            Log.e(TAG, "Error searching files", e);
        }
        return results;
    }
    
    private void searchFilesRecursive(File directory, String pattern, JSONArray results) {
        if (!directory.isDirectory()) return;
        
        File[] files = directory.listFiles();
        if (files != null) {
            for (File file : files) {
                try {
                    if (file.getName().toLowerCase().contains(pattern)) {
                        JSONObject fileInfo = new JSONObject();
                        fileInfo.put("name", file.getName());
                        fileInfo.put("path", file.getAbsolutePath());
                        fileInfo.put("size", file.length());
                        fileInfo.put("is_directory", file.isDirectory());
                        results.put(fileInfo);
                    }
                    
                    if (file.isDirectory()) {
                        searchFilesRecursive(file, pattern, results);
                    }
                } catch (Exception e) {
                    Log.e(TAG, "Error in recursive search", e);
                }
            }
        }
    }
    
    /**
     * Get file tree structure
     */
    public JSONObject getFileTree(String path, int maxDepth) {
        JSONObject tree = new JSONObject();
        try {
            File root = new File(path);
            if (root.exists()) {
                tree.put("name", root.getName());
                tree.put("path", root.getAbsolutePath());
                tree.put("is_directory", root.isDirectory());
                
                if (root.isDirectory() && maxDepth > 0) {
                    JSONArray children = new JSONArray();
                    File[] files = root.listFiles();
                    if (files != null) {
                        for (File file : files) {
                            children.put(getFileTree(file.getAbsolutePath(), maxDepth - 1));
                        }
                    }
                    tree.put("children", children);
                } else {
                    tree.put("size", root.length());
                }
            }
        } catch (Exception e) {
            Log.e(TAG, "Error building file tree", e);
        }
        return tree;
    }
    
    /**
     * Read file content
     */
    public String readFile(String path) {
        StringBuilder content = new StringBuilder();
        try {
            FileInputStream fis = new FileInputStream(path);
            byte[] buffer = new byte[1024];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                content.append(new String(buffer, 0, bytesRead));
            }
            fis.close();
        } catch (Exception e) {
            Log.e(TAG, "Error reading file", e);
            return null;
        }
        return content.toString();
    }
    
    /**
     * Write content to file
     */
    public boolean writeFile(String path, String content) {
        try {
            FileOutputStream fos = new FileOutputStream(path);
            fos.write(content.getBytes());
            fos.close();
            return true;
        } catch (Exception e) {
            Log.e(TAG, "Error writing file", e);
            return false;
        }
    }
    
    /**
     * Copy file
     */
    public boolean copyFile(String sourcePath, String destPath) {
        try {
            FileInputStream fis = new FileInputStream(sourcePath);
            FileOutputStream fos = new FileOutputStream(destPath);
            
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                fos.write(buffer, 0, bytesRead);
            }
            
            fis.close();
            fos.close();
            return true;
        } catch (Exception e) {
            Log.e(TAG, "Error copying file", e);
            return false;
        }
    }
    
    /**
     * Move file
     */
    public boolean moveFile(String sourcePath, String destPath) {
        File source = new File(sourcePath);
        File dest = new File(destPath);
        return source.renameTo(dest);
    }
    
    /**
     * Delete file or directory
     */
    public boolean deleteFile(String path) {
        return deleteRecursive(new File(path));
    }
    
    private boolean deleteRecursive(File file) {
        if (file.isDirectory()) {
            File[] files = file.listFiles();
            if (files != null) {
                for (File child : files) {
                    deleteRecursive(child);
                }
            }
        }
        return file.delete();
    }
    
    /**
     * Create directory
     */
    public boolean createDirectory(String path) {
        File dir = new File(path);
        return dir.mkdirs();
    }
    
    /**
     * Compress files to ZIP
     */
    public boolean compressToZip(List<String> filePaths, String outputZipPath) {
        try {
            FileOutputStream fos = new FileOutputStream(outputZipPath);
            ZipOutputStream zos = new ZipOutputStream(fos);
            
            for (String filePath : filePaths) {
                File file = new File(filePath);
                if (!file.exists()) continue;
                
                FileInputStream fis = new FileInputStream(file);
                ZipEntry entry = new ZipEntry(file.getName());
                zos.putNextEntry(entry);
                
                byte[] buffer = new byte[4096];
                int bytesRead;
                while ((bytesRead = fis.read(buffer)) != -1) {
                    zos.write(buffer, 0, bytesRead);
                }
                
                fis.close();
                zos.closeEntry();
            }
            
            zos.close();
            fos.close();
            return true;
        } catch (Exception e) {
            Log.e(TAG, "Error compressing files", e);
            return false;
        }
    }
    
    /**
     * Extract ZIP file
     */
    public boolean extractZip(String zipPath, String outputDir) {
        try {
            File dir = new File(outputDir);
            if (!dir.exists()) dir.mkdirs();
            
            FileInputStream fis = new FileInputStream(zipPath);
            ZipInputStream zis = new ZipInputStream(fis);
            ZipEntry entry;
            
            while ((entry = zis.getNextEntry()) != null) {
                String filePath = outputDir + File.separator + entry.getName();
                
                if (entry.isDirectory()) {
                    new File(filePath).mkdirs();
                } else {
                    FileOutputStream fos = new FileOutputStream(filePath);
                    byte[] buffer = new byte[4096];
                    int bytesRead;
                    while ((bytesRead = zis.read(buffer)) != -1) {
                        fos.write(buffer, 0, bytesRead);
                    }
                    fos.close();
                }
                zis.closeEntry();
            }
            
            zis.close();
            fis.close();
            return true;
        } catch (Exception e) {
            Log.e(TAG, "Error extracting ZIP", e);
            return false;
        }
    }
    
    /**
     * Get storage info
     */
    public JSONObject getStorageInfo() {
        JSONObject info = new JSONObject();
        try {
            // Internal storage
            File internal = Environment.getDataDirectory();
            info.put("internal_total", internal.getTotalSpace());
            info.put("internal_free", internal.getFreeSpace());
            info.put("internal_used", internal.getTotalSpace() - internal.getFreeSpace());
            
            // External storage
            if (Environment.getExternalStorageState().equals(Environment.MEDIA_MOUNTED)) {
                File external = Environment.getExternalStorageDirectory();
                info.put("external_total", external.getTotalSpace());
                info.put("external_free", external.getFreeSpace());
                info.put("external_used", external.getTotalSpace() - external.getFreeSpace());
            }
            
            // SD card paths
            JSONArray paths = new JSONArray();
            paths.put(Environment.getExternalStorageDirectory().getAbsolutePath());
            paths.put(context.getExternalFilesDir(null).getAbsolutePath());
            info.put("storage_paths", paths);
            
        } catch (Exception e) {
            Log.e(TAG, "Error getting storage info", e);
        }
        return info;
    }
    
    /**
     * Find files by extension
     */
    public JSONArray findFilesByExtension(String rootPath, String extension) {
        JSONArray results = new JSONArray();
        try {
            findByExtensionRecursive(new File(rootPath), extension.toLowerCase(), results);
        } catch (Exception e) {
            Log.e(TAG, "Error finding files by extension", e);
        }
        return results;
    }
    
    private void findByExtensionRecursive(File directory, String extension, JSONArray results) {
        if (!directory.isDirectory()) return;
        
        File[] files = directory.listFiles();
        if (files != null) {
            for (File file : files) {
                try {
                    if (file.isFile() && file.getName().toLowerCase().endsWith(extension)) {
                        JSONObject fileInfo = new JSONObject();
                        fileInfo.put("name", file.getName());
                        fileInfo.put("path", file.getAbsolutePath());
                        fileInfo.put("size", file.length());
                        results.put(fileInfo);
                    }
                    
                    if (file.isDirectory()) {
                        findByExtensionRecursive(file, extension, results);
                    }
                } catch (Exception e) {
                    Log.e(TAG, "Error in extension search", e);
                }
            }
        }
    }
    
    /**
     * Get file permissions
     */
    public JSONObject getFilePermissions(String path) {
        JSONObject permissions = new JSONObject();
        try {
            File file = new File(path);
            permissions.put("readable", file.canRead());
            permissions.put("writable", file.canWrite());
            permissions.put("executable", file.canExecute());
            permissions.put("hidden", file.isHidden());
        } catch (Exception e) {
            Log.e(TAG, "Error getting file permissions", e);
        }
        return permissions;
    }
    
    /**
     * Calculate directory size
     */
    public long getDirectorySize(File directory) {
        long size = 0;
        if (directory.isDirectory()) {
            File[] files = directory.listFiles();
            if (files != null) {
                for (File file : files) {
                    if (file.isFile()) {
                        size += file.length();
                    } else {
                        size += getDirectorySize(file);
                    }
                }
            }
        } else {
            size = directory.length();
        }
        return size;
    }
}
