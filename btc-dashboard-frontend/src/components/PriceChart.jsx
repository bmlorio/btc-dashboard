import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Area,
  AreaChart
} from 'recharts';
import { TrendingUp, Calendar, BarChart3 } from 'lucide-react';

const PriceChart = ({ fullWidth = false }) => {
  const [timeframe, setTimeframe] = useState('24h');
  const [chartData, setChartData] = useState([]);

  // Generar datos de ejemplo para el gráfico
  useEffect(() => {
    const generateData = () => {
      const now = new Date();
      const data = [];
      const points = timeframe === '24h' ? 24 : timeframe === '7d' ? 7 : 30;
      
      let basePrice = 67850;
      
      for (let i = points; i >= 0; i--) {
        const date = new Date(now);
        if (timeframe === '24h') {
          date.setHours(date.getHours() - i);
        } else if (timeframe === '7d') {
          date.setDate(date.getDate() - i);
        } else {
          date.setDate(date.getDate() - i);
        }
        
        // Simular variación de precio
        const variation = (Math.random() - 0.5) * 2000;
        basePrice += variation;
        
        data.push({
          time: timeframe === '24h' 
            ? date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
            : date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric' }),
          price: Math.max(basePrice, 50000), // Precio mínimo
          volume: Math.random() * 1000000000,
          timestamp: date.getTime()
        });
      }
      
      return data.sort((a, b) => a.timestamp - b.timestamp);
    };

    setChartData(generateData());
  }, [timeframe]);

  const formatPrice = (value) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  };

  const formatVolume = (value) => {
    return new Intl.NumberFormat('es-ES', {
      notation: 'compact',
      maximumFractionDigits: 1
    }).format(value);
  };

  const currentPrice = chartData.length > 0 ? chartData[chartData.length - 1].price : 0;
  const firstPrice = chartData.length > 0 ? chartData[0].price : 0;
  const priceChange = currentPrice - firstPrice;
  const priceChangePercent = firstPrice > 0 ? (priceChange / firstPrice) * 100 : 0;

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white border border-gray-200 rounded-lg p-3 shadow-sm">
          <p className="text-gray-800 text-sm font-medium">{label}</p>
          <p className="text-orange-600 text-sm">
            Precio: {formatPrice(payload[0].value)}
          </p>
          {payload[1] && (
            <p className="text-blue-600 text-sm">
              Volumen: ${formatVolume(payload[1].value)}
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <Card className={`bg-white border border-gray-200 shadow-sm ${fullWidth ? 'col-span-full' : ''}`}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-gray-800 flex items-center space-x-2">
              <BarChart3 className="h-5 w-5 text-orange-600" />
              <span>Gráfico de Precios BTC/USD</span>
            </CardTitle>
            <CardDescription className="text-gray-500">
              Evolución del precio en tiempo real
            </CardDescription>
          </div>
          
          <div className="flex items-center space-x-2">
            <div className="flex items-center space-x-1">
              {priceChange >= 0 ? (
                <TrendingUp className="h-4 w-4 text-green-600" />
              ) : (
                <TrendingUp className="h-4 w-4 text-red-600 rotate-180" />
              )}
              <span className={`text-sm font-medium ${
                priceChange >= 0 ? 'text-green-600' : 'text-red-600'
              }`}>
                {priceChangePercent >= 0 ? '+' : ''}{priceChangePercent.toFixed(2)}%
              </span>
            </div>
          </div>
        </div>
        
        {/* Timeframe Selector */}
        <div className="flex space-x-2 mt-4">
            {['24h', '7d', '30d'].map((tf) => (
            <Button
              key={tf}
              variant={timeframe === tf ? "default" : "outline"}
              size="sm"
              onClick={() => setTimeframe(tf)}
              className={timeframe === tf 
                ? "bg-orange-600 hover:bg-orange-700 text-white" 
                : "border-gray-200 text-gray-700 hover:bg-gray-100"
              }
            >
              {tf}
            </Button>
          ))}
        </div>
      </CardHeader>
      
      <CardContent>
  <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="priceGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f97316" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#f97316" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
              <XAxis 
                dataKey="time" 
                stroke="#9CA3AF"
                fontSize={12}
                tickLine={false}
                axisLine={false}
              />
              <YAxis 
                stroke="#9CA3AF"
                fontSize={12}
                tickLine={false}
                axisLine={false}
                tickFormatter={formatPrice}
                domain={['dataMin - 1000', 'dataMax + 1000']}
              />
              <Tooltip content={<CustomTooltip />} />
              <Area
                type="monotone"
                dataKey="price"
                stroke="#f97316"
                strokeWidth={2}
                fill="url(#priceGradient)"
                dot={false}
                activeDot={{ r: 4, fill: "#f97316", stroke: "#fff", strokeWidth: 2 }}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
        
        {/* Price Stats */}
        <div className="grid grid-cols-3 gap-4 mt-4 pt-4 border-t border-gray-200">
          <div className="text-center">
            <div className="text-sm text-gray-500">Precio Actual</div>
            <div className="text-lg font-semibold text-gray-900">
              {formatPrice(currentPrice)}
            </div>
          </div>
          <div className="text-center">
            <div className="text-sm text-gray-500">Máximo {timeframe}</div>
            <div className="text-lg font-semibold text-green-600">
              {formatPrice(Math.max(...chartData.map(d => d.price)))}
            </div>
          </div>
          <div className="text-center">
            <div className="text-sm text-gray-500">Mínimo {timeframe}</div>
            <div className="text-lg font-semibold text-red-600">
              {formatPrice(Math.min(...chartData.map(d => d.price)))}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default PriceChart;

