import React from 'react';

interface SpinnerProps {
  size?: string; // Size of the spinner, default is '50px'
  color?: string; // Color of the spinner, default is blue
  className?: string; // Custom class for additional styling
}

const Spinner: React.FC<SpinnerProps> = ({ size = '50px', color = 'blue', className = '' }) => {
  return (
    <div
      className={`animate-spin border-4 border-t-transparent border-${color}-500 border-solid rounded-full ${className}`}
      style={{
        width: size,
        height: size,
        borderColor: `transparent ${color} transparent transparent`, // custom color for the spinner
      }}
    />
  );
};

export default Spinner;
