"use client";

import { useState, useEffect, useMemo } from "react";
import ResearchList from "./ResearchList";

const ITEMS_PER_PAGE = 20;

export default function ResearchClient() {
  const [allResearch, setAllResearch] = useState<any[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [page, setPage] = useState(1);

  // Fetch all research on mount
  useEffect(() => {
    async function fetchResearch() {
      try {
        const res = await fetch("/api/research");
        if (!res.ok) throw new Error("Failed to fetch research");
        const data = await res.json();
        setAllResearch(data);
      } catch (error) {
        console.error("Error fetching research:", error);
        setAllResearch([]);
      }
    }
    fetchResearch();
  }, []);

  // Filter by search query
  const filtered = useMemo(() => {
    if (!searchQuery.trim()) return allResearch;
    const q = searchQuery.toLowerCase();
    return allResearch.filter(
      (item) =>
        item.title.toLowerCase().includes(q) ||
        item.excerpt.toLowerCase().includes(q) ||
        item.slug.toLowerCase().includes(q)
    );
  }, [allResearch, searchQuery]);

  const totalPages = Math.ceil(filtered.length / ITEMS_PER_PAGE);
  const start = (page - 1) * ITEMS_PER_PAGE;
  const paged = filtered.slice(start, start + ITEMS_PER_PAGE);

  // Reset to page 1 when search changes
  useEffect(() => {
    setPage(1);
  }, [searchQuery]);

  return (
    <div className="space-y-6">
      {/* Search input */}
      <div className="flex justify-center">
        <input
          type="text"
          placeholder="Search research..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full max-w-md px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-ring"
        />
      </div>

      {/* Results count */}
      <p className="text-sm text-muted-foreground text-center">
        {filtered.length} result{filtered.length !== 1 ? "s" : ""} found
        {searchQuery && ` for "${searchQuery}"`}
        {totalPages > 1 && ` (page ${page} of ${totalPages})`}
      </p>

      {/* Research list */}
      <ResearchList items={paged} />

      {/* Pagination controls */}
      {totalPages > 1 && (
        <div className="flex justify-center items-center gap-4">
          <button
            onClick={() => setPage((p) => Math.max(p - 1, 1))}
            disabled={page === 1}
            className="px-4 py-2 border rounded disabled:opacity-50"
          >
            Previous
          </button>
          <span>
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
            disabled={page === totalPages}
            className="px-4 py-2 border rounded disabled:opacity-50"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}
