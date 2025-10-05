// Hook encapsulating the state management for the Gemini lesson outline form.
// The labs emphasise isolating fetch logic inside hooks so components stay
// presentational and easy to reuse in lectures.
import { useCallback, useState } from 'react';

import { post } from '../../../lib/api';

const ENDPOINT = '/ai/lesson-outline';

/**
 * Manage the lesson outline form lifecycle.
 *
 * @returns {object} Handlers and state consumed by the presentational component.
 */
export function useLessonOutlineForm() {
  const [topic, setTopic] = useState('');
  const [outline, setOutline] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = useCallback(
    async (event) => {
      event.preventDefault();
      const trimmedTopic = topic.trim();
      if (!trimmedTopic) {
        setError('Please enter a topic.');
        setOutline([]);
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const response = await post(ENDPOINT, { topic: trimmedTopic });
        setOutline(Array.isArray(response.outline) ? response.outline : []);
      } catch (err) {
        setOutline([]);
        const detailMessage =
          typeof err?.detail === 'string'
            ? err.detail
            : err instanceof Error && err.message
              ? err.message
              : 'Unknown error';
        setError(detailMessage);
      } finally {
        setLoading(false);
      }
    },
    [topic]
  );

  return {
    topic,
    setTopic,
    outline,
    loading,
    error,
    handleSubmit
  };
}
