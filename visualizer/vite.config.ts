import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => ({
  plugins: [react()],
  base: './',
  build:
    mode === 'library'
      ? {
          outDir: 'dist',
          lib: {
            entry: 'src/index.ts',
            formats: ['es'],
            fileName: 'experiment-viewer',
            cssFileName: 'experiment-viewer',
          },
          rollupOptions: {
            external: ['react', 'react-dom', 'react/jsx-runtime'],
          },
        }
      : { outDir: 'site' },
}));
