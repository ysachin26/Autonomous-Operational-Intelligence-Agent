
# ASLOA: AI Sales Lead Orchestration Agent

## Overview

This application, ASLOA (AI Sales Lead Orchestration Agent), is a React-based tool for analyzing sales leads. It captures lead information through a form and provides an AI-powered analysis, including lead scoring, BANT qualification, suggested outreach, and routing recommendations.

## Implemented Features

*   Lead capture form with fields for person, company, and notes.
*   Initial implementation with mock data for AI analysis.
*   UI to display analysis results, including score, BANT status, outreach, and routing.
*   Dropdown validation fix.

## Current Plan: Integrate Agentic.ai

1.  Install the `@agentic/react` package.
2.  Add `VITE_AGENTIC_API_KEY` to `.env` and `.idx/dev.nix`.
3.  Update `App.jsx` to use real AI agents instead of the mock function.
4.  Define agents for:
    *   **Lead Scoring**: To generate a score and fit label.
    *   **BANT Qualification**: To analyze Budget, Authority, Need, and Timeline.
    *   **Outreach Generation**: To create a sample outreach email subject.
    *   **Lead Routing**: To determine priority and segment.
5.  Modify the `handleSubmit` function to call these agents and process the results.
6.  Ensure error handling for the API calls.
