interface SpinnerProps {
    size?: string;
    color?: string;
    className?: string;
  }
  
  const Spinner: React.FC<SpinnerProps> = ({ size = '50px', color = 'blue', className = '' }) => {
    return (
      <div className="absolute inset-0 flex items-center justify-center flex-col z-20">
        <div
          className={`animate-spin border-4 border-t-transparent border-${color}-500 border-solid rounded-full ${className}`}
          style={{
            width: size,
            height: size,
            borderColor: `transparent ${color} transparent transparent`, // custom color for the spinner
          }}
        />
        <p className="mt-2 text-gray-700">Waiting for prediction...</p>
      </div>
    );
  };
  
  export default Spinner;
  