import React, { useEffect } from 'react';
import { useRouter } from 'next/router';

export default function IndexPage() {
  const router = useRouter();

  useEffect(() => {
    router.push('/basic');
  }, [router]);

  return (
    <div className="flex h-screen items-center justify-center">
      <div className="text-center">
        <h1 className="text-xl font-semibold mb-2">Loading Flight Assistance...</h1>
        <p>Please wait while we redirect you to the flight assistant.</p>
      </div>
    </div>
  );
}
