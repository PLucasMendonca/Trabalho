"use client";

import { createContext, useState, useContext, useEffect } from "react";

type FileWithUrl = {
  file: File;
  url: string;
};

type AppContextType = {
  importedFile: FileWithUrl[];
  setImportedFile: React.Dispatch<React.SetStateAction<FileWithUrl[]>>;
};

const AppContext = createContext<AppContextType>({
  importedFile: [],
  setImportedFile: () => { },
});

export function AppWrapper({ children }: { children: React.ReactNode }) {
  const [importedFile, setImportedFile] = useState<FileWithUrl[]>([]);

  useEffect(() => {
    if (importedFile.length > 1) {
      setImportedFile((prev) => {
        const newFiles = [...prev];
        newFiles.splice(0, 1);
        return newFiles;
      });
    }

  }, [importedFile]);

  return (
    <AppContext.Provider value={{ importedFile, setImportedFile }}>
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext() {
  return useContext(AppContext);
}
