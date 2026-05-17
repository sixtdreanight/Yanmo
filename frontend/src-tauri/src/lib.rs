use tauri::Manager;
use std::process::{Command, Child};
use std::sync::Mutex;


struct PythonBackend(Mutex<Option<Child>>);

impl Drop for PythonBackend {
    fn drop(&mut self) {
        if let Ok(mut guard) = self.0.lock() {
            if let Some(ref mut child) = *guard {
                let _ = child.kill();
            }
        }
    }
}

fn find_python() -> &'static str {
    #[cfg(target_os = "windows")]
    { "python" }
    #[cfg(not(target_os = "windows"))]
    { "python3" }
}

fn start_backend() -> Option<Child> {
    // Try the system python first
    if let Ok(child) = Command::new(find_python())
        .args(["-m", "backend.main"])
        .spawn()
    {
        return Some(child);
    }
    // Fallback: try plain 'python'
    if let Ok(child) = Command::new("python")
        .args(["-m", "backend.main"])
        .spawn()
    {
        return Some(child);
    }
    None
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_opener::init())
        .setup(|app| {
            let backend = start_backend();
            app.manage(PythonBackend(Mutex::new(backend)));
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
