import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Home from '../pages/index';

test('renders welcome message', () => {
  render(<Home />);
  expect(screen.getByText(/welcome/i)).toBeInTheDocument();
});