import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { 
  PieChart, 
  Pie, 
  Cell, 
  ResponsiveContainer, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip 
} from 'recharts';
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  Users, 
  Zap, 
  Globe,
  AlertTriangle,
  Target
} from 'lucide-react';

const MarketMetrics = ({ fullWidth = false }) => {
  const [metrics, setMetrics] = useState({
    openInterest: 15420000000,
    fundingRate: 0.0125,
    longShortRatio: 2.3,
    liquidations24h: 125000000,
    dominance: 54.2,
    volatility: 3.8,
    volume24h: 28500000000,
    activeAddresses: 1250000
  });

  // Datos para el gráfico de funding rates por exchange
  const fundingRatesData = [
    { exchange: 'Binance', rate: 0.0125, color: '#f59e0b' },
    { exchange: 'Bybit', rate: 0.0089, color: '#3b82f6' },
    { exchange: 'OKX', rate: 0.0156, color: '#10b981' },
    { exchange: 'Bitget', rate: 0.0098, color: '#8b5cf6' },
    { exchange: 'dYdX', rate: 0.0203, color: '#ef4444' }
  ];

  // Datos para el gráfico de liquidaciones
  const liquidationsData = [
    { time: '00:00', longs: 15000000, shorts: 8000000 },
    { time: '04:00', longs: 22000000, shorts: 12000000 },
    { time: '08:00', longs: 18000000, shorts: 15000000 },
    { time: '12:00', longs: 35000000, shorts: 20000000 },
    { time: '16:00', longs: 28000000, shorts: 18000000 },
    { time: '20:00', longs: 25000000, shorts: 22000000 }
  ];

  // Datos para el gráfico de dominancia
  const dominanceData = [
    { name: 'Bitcoin', value: 54.2, color: '#f97316' },
    { name: 'Ethereum', value: 17.8, color: '#3b82f6' },
    { name: 'Otros', value: 28.0, color: '#6b7280' }
  ];

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'USD',
      notation: 'compact',
      maximumFractionDigits: 1
    }).format(value);
  };

  const formatNumber = (value) => {
    return new Intl.NumberFormat('es-ES', {
      notation: 'compact',
      maximumFractionDigits: 1
    }).format(value);
  };

  const formatPercentage = (value) => {
    return `${value >= 0 ? '+' : ''}${value.toFixed(3)}%`;
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white border border-gray-200 rounded-lg p-3 shadow-sm">
          <p className="text-gray-800 text-sm font-medium">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: {formatCurrency(entry.value)}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className={`space-y-6 ${fullWidth ? 'col-span-full' : ''}`}>
      {/* Métricas principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="bg-white border border-gray-200 shadow-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-700">
              Open Interest
            </CardTitle>
            <Target className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">
              {formatCurrency(metrics.openInterest)}
            </div>
            <div className="flex items-center space-x-2 mt-2">
              <TrendingUp className="h-4 w-4 text-green-600" />
              <span className="text-sm text-green-600">+5.2%</span>
              <span className="text-xs text-gray-500">24h</span>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-white border border-gray-200 shadow-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-700">
              Funding Rate
            </CardTitle>
            <Zap className="h-4 w-4 text-amber-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">
              {formatPercentage(metrics.fundingRate)}
            </div>
            <div className="flex items-center space-x-2 mt-2">
              <Badge variant="secondary" className="bg-amber-100 text-amber-700 border-amber-200">
                Neutral
              </Badge>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-white border border-gray-200 shadow-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-700">
              Long/Short Ratio
            </CardTitle>
            <Users className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">
              {metrics.longShortRatio.toFixed(1)}:1
            </div>
            <div className="mt-2">
              <Progress 
                value={70} 
                className="h-2 bg-gray-200"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>Longs: 70%</span>
                <span>Shorts: 30%</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-white border border-gray-200 shadow-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-700">
              Liquidaciones 24h
            </CardTitle>
            <AlertTriangle className="h-4 w-4 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">
              {formatCurrency(metrics.liquidations24h)}
            </div>
            <div className="flex items-center space-x-2 mt-2">
              <TrendingDown className="h-4 w-4 text-red-600" />
              <span className="text-sm text-red-600">-12.3%</span>
              <span className="text-xs text-gray-500">vs ayer</span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Gráficos */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Funding Rates por Exchange */}
        <Card className="bg-white border border-gray-200 shadow-sm">
          <CardHeader>
            <CardTitle className="text-gray-800 flex items-center space-x-2">
              <Zap className="h-5 w-5 text-yellow-500" />
              <span>Funding Rates por Exchange</span>
            </CardTitle>
            <CardDescription className="text-gray-500">
              Tasas de financiamiento actuales
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={fundingRatesData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" opacity={0.6} />
                  <XAxis 
                    dataKey="exchange" 
                    stroke="#6B7280"
                    fontSize={12}
                    tickLine={false}
                    axisLine={false}
                  />
                  <YAxis 
                    stroke="#6B7280"
                    fontSize={12}
                    tickLine={false}
                    axisLine={false}
                    tickFormatter={(value) => `${(value * 100).toFixed(2)}%`}
                  />
                  <Tooltip 
                    content={({ active, payload, label }) => {
                      if (active && payload && payload.length) {
                        return (
                          <div className="bg-white border border-gray-200 rounded-lg p-3 shadow-sm">
                            <p className="text-gray-800 text-sm font-medium">{label}</p>
                            <p className="text-yellow-600 text-sm">
                              Rate: {(payload[0].value * 100).toFixed(3)}%
                            </p>
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                  <Bar dataKey="rate" radius={[4, 4, 0, 0]}>
                    {fundingRatesData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Dominancia del Mercado */}
        <Card className="bg-white border border-gray-200 shadow-sm">
          <CardHeader>
            <CardTitle className="text-gray-800 flex items-center space-x-2">
              <Globe className="h-5 w-5 text-blue-500" />
              <span>Dominancia del Mercado</span>
            </CardTitle>
            <CardDescription className="text-gray-500">
              Distribución de capitalización de mercado
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={dominanceData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {dominanceData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        return (
                          <div className="bg-white border border-gray-200 rounded-lg p-3 shadow-sm">
                            <p className="text-gray-800 text-sm font-medium">{payload[0].payload.name}</p>
                            <p className="text-blue-500 text-sm">
                              {payload[0].value.toFixed(1)}%
                            </p>
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="flex justify-center space-x-4 mt-4">
              {dominanceData.map((item, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <div 
                    className="w-3 h-3 rounded-full" 
                    style={{ backgroundColor: item.color }}
                  />
                  <span className="text-sm text-gray-700">{item.name}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Liquidaciones por hora */}
      <Card className="bg-white border border-gray-200 shadow-sm">
        <CardHeader>
          <CardTitle className="text-gray-800 flex items-center space-x-2">
            <AlertTriangle className="h-5 w-5 text-red-500" />
            <span>Liquidaciones por Hora (24h)</span>
          </CardTitle>
          <CardDescription className="text-gray-500">
            Distribución de liquidaciones de longs vs shorts
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={liquidationsData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" opacity={0.6} />
                <XAxis 
                  dataKey="time" 
                  stroke="#6B7280"
                  fontSize={12}
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis 
                  stroke="#6B7280"
                  fontSize={12}
                  tickLine={false}
                  axisLine={false}
                  tickFormatter={formatCurrency}
                />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="longs" fill="#ef4444" name="Longs" radius={[2, 2, 0, 0]} />
                <Bar dataKey="shorts" fill="#10b981" name="Shorts" radius={[2, 2, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="flex justify-center space-x-6 mt-4">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded-full bg-red-500" />
              <span className="text-sm text-gray-700">Liquidaciones Long</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded-full bg-green-500" />
              <span className="text-sm text-gray-700">Liquidaciones Short</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default MarketMetrics;

