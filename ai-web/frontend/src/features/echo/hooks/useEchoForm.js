// Custom React hook that encapsulates the state and network calls for the echo form.
//
// Lab 02 encourages students to colocate hooks with the feature they support. This
// implementation demonstrates that pattern by keeping the request logic next to
// the UI while exposing a tiny API that the component can consume.
import { useCallback, useState } from 'react';

import { post } from '../../../lib/api';
import { withRetry } from '../../../lib/retry';

const DEFAULT_FAILURES = 2; // Fail twice before succeeding so the retry flow is visible.

export function useEchoForm({ failures = DEFAULT_FAILURES } = {}) {
  const [msg, setMsg] = useState('hello'); // Track the text field value.
  const [response, setResponse] = useState(''); // Hold the JSON payload returned from the backend.
  const [loading, setLoading] = useState(false); // Indicate when the form is sending a request.
  const [error, setError] = useState(''); // Store a friendly message if every retry attempt fails.

  const handleSubmit = useCallback(
    async (event) => {
      event?.preventDefault(); // Stop the browser from navigating away when the form submits.
      setLoading(true); // Trigger the loading state immediately so the UI can disable inputs.
      setError(''); // Clear any stale error message from a previous attempt.
      setResponse(''); // Reset the response so old data does not flash between retries.

      try {
        const query = new URLSearchParams({ failures: failures.toString() });
        const json = await withRetry(
          () => post(`/flaky-echo?${query.toString()}`, { msg }),
          failures,
          500,
        );

        // Present the structured JSON so students can see how many attempts were needed.
        setResponse(JSON.stringify(json, null, 2));
      } catch (err) {
        console.error('Echo request failed after retries', err); // Surface useful debugging info for the instructor console.
        setError('A temporary issue was encountered. Please try again.');
      } finally {
        setLoading(false); // Always clear the loading flag once the promise settles.
      }
    },
    [failures, msg],
  );

  return {
    msg,
    setMsg,
    handleSubmit,
    loading,
    error,
    response,
  };
}
