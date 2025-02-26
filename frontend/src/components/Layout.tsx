import React from "react";
import { useIsMobile } from "@/hooks/use-mobile";

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const isMobile = useIsMobile();
  
  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center">
          <div className="flex items-center space-x-2">
            <img src="/robot.svg" alt="Reachy Logo" className="h-8 w-8" />
            <span className="font-bold text-xl">Reachy Function Calling</span>
          </div>
          
          <div className="flex-1"></div>
          
          <nav className="flex items-center space-x-4">
            <a 
              href="https://github.com/yourusername/reachy-function-calling" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-muted-foreground hover:text-foreground transition-colors"
            >
              GitHub
            </a>
          </nav>
        </div>
      </header>
      
      {/* Main Content */}
      <main className="flex-1 container py-4">
        {children}
      </main>
      
      {/* Footer */}
      <footer className="border-t border-border/40 py-4 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex flex-col md:flex-row items-center justify-between">
          <p className="text-sm text-muted-foreground">
            &copy; {new Date().getFullYear()} Reachy Function Calling
          </p>
          <p className="text-sm text-muted-foreground mt-2 md:mt-0">
            Built with React, TailwindCSS, and Reachy 2
          </p>
        </div>
      </footer>
    </div>
  );
}; 