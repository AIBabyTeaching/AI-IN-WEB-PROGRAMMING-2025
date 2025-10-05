// Application shell responsible for wiring feature modules into the page.
//
// Each lab encourages keeping this component small so students can focus on the
// feature folders under `src/features`. New demos should follow the same
// pattern: create a hook for stateful logic and pass it into a presentational
// component.
import { EchoForm } from './features/echo/components/EchoForm';
import { useEchoForm } from './features/echo/hooks/useEchoForm';
import { LessonOutlineForm } from './features/gemini/components/LessonOutlineForm';
import { useLessonOutlineForm } from './features/gemini/hooks/useLessonOutlineForm';

function App() {
  const echoForm = useEchoForm();
  const lessonOutlineForm = useLessonOutlineForm();

  return (
    <main style={{ padding: 24, display: 'grid', gap: 32 }}>
      <header style={{ display: 'grid', gap: 8 }}>
        <h1>AI in Web Programming Demos</h1>
        <p>
          Use these examples to show students how the FastAPI and React layers
          evolve together. Each section mirrors the workflow documented in the
          instructor guide.
        </p>
      </header>

      <section style={{ display: 'grid', gap: 16 }}>
        <h2>Retrying echo service</h2>
        <EchoForm {...echoForm} />
      </section>

      <section style={{ display: 'grid', gap: 16 }}>
        <h2>Gemini lesson outline builder</h2>
        <LessonOutlineForm {...lessonOutlineForm} />
      </section>
    </main>
  );
}

export default App;
