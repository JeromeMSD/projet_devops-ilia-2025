import '@testing-library/jest-dom';
import { render, screen } from "@testing-library/react";
import { test, expect, vi, describe } from 'vitest';
import IncidentsPage from "./IncidentsPage";

vi.mock("../mocks/mockIncidents", () => ({
  mockIncidents: [
    {
      id: "INC-001",
      title: "Panne de la base de données principale",
      sev: 1,
      services: ["db", "backend"],
      summary: "La base de données principale ne répond plus.",
      status: "open",
      started_at: 1730073600,
      commander: "f6c74e13-8b4a-4b63-bf58-1c59a0c21840",
    },
    {
      id: "INC-002",
      title: "Latence API Europe",
      sev: 2,
      services: ["api"],
      summary: "Les temps de réponse API dépassaient 2s en EU-West.",
      status: "resolved",
      started_at: 1730077200,
      commander: "a3d11f92-4b76-46c0-9e83-6f23a28c91a0",
    },
  ],
}));

describe("IncidentsPage", () => {
  test("affiche le titre principal", () => {
    render(<IncidentsPage />);
    expect(screen.getByText(/Incidents récents/i)).toBeInTheDocument();
  });

  test("affiche tous les titres et statuts des incidents", () => {
    render(<IncidentsPage />);
    expect(screen.getByText(/Panne de la base de données principale/i)).toBeInTheDocument();
    expect(screen.getByText(/Latence API Europe/i)).toBeInTheDocument();
    expect(screen.getByText(/open/i)).toBeInTheDocument();
    expect(screen.getByText(/resolved/i)).toBeInTheDocument();
  });

  test("affiche summary, services, sévérité, date et commandant", () => {
    render(<IncidentsPage />);
    // Summary
    expect(screen.getByText(/La base de données principale ne répond plus./i)).toBeInTheDocument();
    expect(screen.getByText(/Les temps de réponse API dépassaient 2s en EU-West./i)).toBeInTheDocument();
    // Services
    expect(screen.getByText(/db, backend/i)).toBeInTheDocument();
    expect(screen.getByText(/api/i)).toBeInTheDocument();
    // Sévérité
    expect(screen.getByText(/Sévérité 1/i)).toBeInTheDocument();
    expect(screen.getByText(/Sévérité 2/i)).toBeInTheDocument();
    // Commandant
    expect(screen.getByText(/f6c74e13-8b4a-4b63-bf58-1c59a0c21840/i)).toBeInTheDocument();
    expect(screen.getByText(/a3d11f92-4b76-46c0-9e83-6f23a28c91a0/i)).toBeInTheDocument();
    // Date (on peut juste vérifier l'année pour rester générique)
    expect(screen.getByText(/2024/i)).toBeInTheDocument();
  });
});
