import Link from "next/link";


export default function Home() {
  return (
<div className="min-h-screen bg-gray-100">
  {/* Hero Section */}
  <div className="bg-blue-600 text-white py-20">
    <div className="container mx-auto text-center">
      <h1 className="text-4xl font-bold mb-4">
        Take Control of Your Health Today
      </h1>
      <p className="text-lg mb-8">
        Fill out our quick health assessment form to understand your health status and explore medical insurance options tailored for you.
      </p>
  
      <Link className="bg-white text-blue-600 py-3 px-6 rounded-lg font-semibold hover:bg-gray-100 transition duration-300" href="/stepper">
            
        
      
        Get Started
      
      </Link>
    </div>
  </div>

  {/* Benefits Section */}
  <div className="container mx-auto py-16">
    <h2 className="text-3xl font-bold mb-8 text-center">
      Why Fill Out This Form?
    </h2>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
      <div className="p-6 bg-white rounded-lg shadow-md">
        <h3 className="text-xl font-semibold mb-4">Health Assessment</h3>
        <p className="text-gray-600">
          Get a detailed analysis of your health status and personalized recommendations.
        </p>
      </div>
      <div className="p-6 bg-white rounded-lg shadow-md">
        <h3 className="text-xl font-semibold mb-4">Insurance Options</h3>
        <p className="text-gray-600">
          Explore medical insurance plans tailored to your needs and budget.
        </p>
      </div>
      <div className="p-6 bg-white rounded-lg shadow-md">
        <h3 className="text-xl font-semibold mb-4">Peace of Mind</h3>
        <p className="text-gray-600">
          Ensure you and your family are protected with the right health coverage.
        </p>
      </div>
    </div>
  </div>

  {/* Trust Signals Section */}
  <div className="bg-gray-50 py-16">
    <div className="container mx-auto text-center">
      <h2 className="text-3xl font-bold mb-8">Trusted by Thousands</h2>
      <div className="flex justify-center space-x-12">
        <img src="/logo1.png" alt="Trusted Partner 1" className="h-12" />
        <img src="/logo2.png" alt="Trusted Partner 2" className="h-12" />
        <img src="/logo3.png" alt="Trusted Partner 3" className="h-12" />
      </div>
    </div>
  </div>

  {/* Footer */}
  <div className="bg-gray-800 text-white py-8">
    <div className="container mx-auto text-center">
      <p className="mb-4">
        &copy; 2023 Health Assessment Platform. All rights reserved.
      </p>
      <p>
        <a href="#" className="text-blue-400 hover:text-blue-300">
          Privacy Policy
        </a>{' '}
        |{' '}
        <a href="#" className="text-blue-400 hover:text-blue-300">
          Terms of Service
        </a>
      </p>
    </div>
  </div>
</div>
  );
}
