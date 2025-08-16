import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  BarChart3, 
  Activity,
  Globe,
  Users,
  AlertTriangle,
  RefreshCw,
  Bitcoin
} from 'lucide-react';
import PriceChart from './PriceChart';
import MarketMetrics from './MarketMetrics';
import SentimentAnalysis from './SentimentAnalysis';
import TradingSignals from './TradingSignals';
import NewsAndSocial from './NewsAndSocial';
import '../App.css';

const Dashboard = () => {
  const [lastUpdate, setLastUpdate] = useState(new Date());
  const [isLoading, setIsLoading] = useState(false);
  const [btcPrice, setBtcPrice] = useState(67850.32);
  const [priceChange, setPriceChange] = useState(2.45);
  const [marketCap, setMarketCap] = useState(1340000000000);

  // Simular actualización de datos
  const refreshData = async () => {
    setIsLoading(true);
    // Simular llamada a API
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Simular nuevos datos
    const newPrice = btcPrice + (Math.random() - 0.5) * 1000;
    const newChange = (Math.random() - 0.5) * 10;
    
    setBtcPrice(newPrice);
    setPriceChange(newChange);
    setLastUpdate(new Date());
    setIsLoading(false);
  };

  // Auto-refresh cada 30 segundos
  useEffect(() => {
    const interval = setInterval(() => {
      refreshData();
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(price);
  };

  const formatMarketCap = (value) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'USD',
      notation: 'compact',
      maximumFractionDigits: 1
    }).format(value);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-gray-50 to-gray-100">
      {/* Header */}
      <header className="border-b border-gray-200 bg-white backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-indigo-600 rounded-lg">
                <Bitcoin className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Dashboard de Bitcoin</h1>
                <p className="text-sm text-gray-600">Sistema de Soporte para Trading</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <div className="text-sm text-gray-600">Última actualización</div>
                <div className="text-sm text-gray-900">
                  {lastUpdate.toLocaleTimeString('es-ES')}
                </div>
              </div>
              <Button 
                onClick={refreshData} 
                disabled={isLoading}
                variant="outline"
                size="sm"
                className="border-gray-200 text-gray-900 hover:bg-gray-100"
              >
                <RefreshCw className={`h-4 w-4 mr-2 text-gray-700 ${isLoading ? 'animate-spin' : ''}`} />
                Actualizar
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6">
        {/* Price Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <Card className="bg-white border border-gray-200 shadow-sm">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-700">
                Precio de Bitcoin
              </CardTitle>
              <DollarSign className="h-4 w-4 text-indigo-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-gray-900">
                {formatPrice(btcPrice)}
              </div>
              <div className="flex items-center space-x-2 mt-2">
                {priceChange >= 0 ? (
                  <TrendingUp className="h-4 w-4 text-green-600" />
                ) : (
                  <TrendingDown className="h-4 w-4 text-red-600" />
                )}
                <span className={`text-sm font-medium ${
                  priceChange >= 0 ? 'text-green-600' : 'text-red-600'
                }`}>
                  {priceChange >= 0 ? '+' : ''}{priceChange.toFixed(2)}%
                </span>
                <span className="text-xs text-gray-500">24h</span>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white border border-gray-200 shadow-sm">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-700">
                Capitalización de Mercado
              </CardTitle>
              <BarChart3 className="h-4 w-4 text-indigo-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-gray-900">
                {formatMarketCap(marketCap)}
              </div>
              <p className="text-xs text-gray-500 mt-2">
                Dominancia: 54.2%
              </p>
            </CardContent>
          </Card>

          <Card className="bg-white border border-gray-200 shadow-sm">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-700">
                Índice de Miedo y Codicia
              </CardTitle>
              <Activity className="h-4 w-4 text-amber-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-gray-900">
                72
              </div>
              <div className="flex items-center space-x-2 mt-2">
                <Badge variant="secondary" className="bg-amber-100 text-amber-700 border-amber-200">
                  Codicia
                </Badge>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Dashboard Tabs */}
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-5 bg-white border border-gray-200 rounded-md">
            <TabsTrigger value="overview" className="text-gray-700 data-[state=active]:bg-indigo-600 data-[state=active]:text-white">
              Resumen
            </TabsTrigger>
            <TabsTrigger value="charts" className="text-gray-700 data-[state=active]:bg-indigo-600 data-[state=active]:text-white">
              Gráficos
            </TabsTrigger>
            <TabsTrigger value="metrics" className="text-gray-700 data-[state=active]:bg-indigo-600 data-[state=active]:text-white">
              Métricas
            </TabsTrigger>
            <TabsTrigger value="sentiment" className="text-gray-700 data-[state=active]:bg-indigo-600 data-[state=active]:text-white">
              Sentimiento
            </TabsTrigger>
            <TabsTrigger value="signals" className="text-gray-700 data-[state=active]:bg-indigo-600 data-[state=active]:text-white">
              Señales
            </TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <PriceChart />
              <MarketMetrics />
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <SentimentAnalysis />
              <NewsAndSocial />
            </div>
          </TabsContent>

          <TabsContent value="charts">
            <PriceChart fullWidth />
          </TabsContent>

          <TabsContent value="metrics">
            <MarketMetrics fullWidth />
          </TabsContent>

          <TabsContent value="sentiment">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <SentimentAnalysis />
              <NewsAndSocial />
            </div>
          </TabsContent>

          <TabsContent value="signals">
            <TradingSignals />
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
};

export default Dashboard;

