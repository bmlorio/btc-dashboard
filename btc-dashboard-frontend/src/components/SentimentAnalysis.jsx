import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { 
  RadialBarChart, 
  RadialBar, 
  ResponsiveContainer, 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip 
} from 'recharts';
import { 
  Heart, 
  TrendingUp, 
  TrendingDown, 
  Users, 
  MessageCircle, 
  ThumbsUp, 
  ThumbsDown,
  Activity,
  Brain
} from 'lucide-react';

const SentimentAnalysis = () => {
  const [sentimentData, setSentimentData] = useState({
    fearGreedIndex: 72,
    socialSentiment: 68,
    redditSentiment: 75,
    twitterSentiment: 62,
    newsAnalysis: 70,
    overallSentiment: 'bullish'
  });

  // Datos históricos del índice de miedo y codicia
  const fearGreedHistory = [
    { date: '15/08', value: 45, label: 'Miedo' },
    { date: '16/08', value: 52, label: 'Neutral' },
    { date: '17/08', value: 58, label: 'Codicia' },
    { date: '18/08', value: 65, label: 'Codicia' },
    { date: '19/08', value: 72, label: 'Codicia' }
  ];

  // Datos de sentimiento por fuente
  const sentimentSources = [
    { 
      name: 'Reddit', 
      value: 75, 
      color: '#ff6b35',
      posts: 1250,
      change: +8.2
    },
    { 
      name: 'Twitter', 
      value: 62, 
      color: '#1da1f2',
      posts: 8500,
      change: -2.1
    },
    { 
      name: 'Noticias', 
      value: 70, 
      color: '#10b981',
      posts: 145,
      change: +5.7
    },
    { 
      name: 'Telegram', 
      value: 68, 
      color: '#0088cc',
      posts: 3200,
      change: +3.4
    }
  ];

  // Datos para el gráfico radial del índice de miedo y codicia
  const fearGreedRadialData = [
    {
      name: 'Fear & Greed',
      value: sentimentData.fearGreedIndex,
      fill: sentimentData.fearGreedIndex > 50 ? '#f59e0b' : '#ef4444'
    }
  ];

  const getSentimentLabel = (value) => {
    if (value <= 25) return { label: 'Miedo Extremo', color: 'text-red-600' };
    if (value <= 45) return { label: 'Miedo', color: 'text-amber-600' };
    if (value <= 55) return { label: 'Neutral', color: 'text-gray-500' };
    if (value <= 75) return { label: 'Codicia', color: 'text-amber-600' };
    return { label: 'Codicia Extrema', color: 'text-green-600' };
  };

  const getSentimentIcon = (value) => {
    if (value > 60) return <TrendingUp className="h-4 w-4 text-green-600" />;
    if (value < 40) return <TrendingDown className="h-4 w-4 text-red-600" />;
    return <Activity className="h-4 w-4 text-amber-600" />;
  };

  const formatNumber = (value) => {
    return new Intl.NumberFormat('es-ES', {
      notation: 'compact',
      maximumFractionDigits: 1
    }).format(value);
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white border border-gray-200 rounded-lg p-3 shadow-sm">
          <p className="text-gray-800 text-sm font-medium">{label}</p>
          <p className="text-amber-600 text-sm">
            Índice: {data.value}
          </p>
          <p className="text-gray-600 text-sm">
            {data.label}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <Card className="bg-white border border-gray-200 shadow-sm">
      <CardHeader>
        <CardTitle className="text-gray-800 flex items-center space-x-2">
          <Brain className="h-5 w-5 text-purple-500" />
          <span>Análisis de Sentimiento</span>
        </CardTitle>
        <CardDescription className="text-gray-500">
          Indicadores de sentimiento del mercado y redes sociales
        </CardDescription>
      </CardHeader>
      
      <CardContent className="space-y-6">
        {/* Índice de Miedo y Codicia */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="text-center">
              <h3 className="text-lg font-semibold text-gray-800 mb-2">
                Índice de Miedo y Codicia
              </h3>
              <div className="h-32">
                <ResponsiveContainer width="100%" height="100%">
                  <RadialBarChart 
                    cx="50%" 
                    cy="50%" 
                    innerRadius="60%" 
                    outerRadius="90%" 
                    data={fearGreedRadialData}
                    startAngle={180}
                    endAngle={0}
                  >
                    <RadialBar 
                      dataKey="value" 
                      cornerRadius={10} 
                      fill={fearGreedRadialData[0].fill}
                    />
                  </RadialBarChart>
                </ResponsiveContainer>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-gray-900">
                  {sentimentData.fearGreedIndex}
                </div>
                <div className={`text-sm font-medium ${getSentimentLabel(sentimentData.fearGreedIndex).color}`}>
                  {getSentimentLabel(sentimentData.fearGreedIndex).label}
                </div>
              </div>
            </div>
          </div>

            <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800">
              Tendencia Histórica (5 días)
            </h3>
            <div className="h-32">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={fearGreedHistory}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                  <XAxis 
                    dataKey="date" 
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
                    domain={[0, 100]}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Line
                    type="monotone"
                    dataKey="value"
                    stroke="#f59e0b"
                    strokeWidth={3}
                    dot={{ fill: "#f59e0b", strokeWidth: 2, r: 4 }}
                    activeDot={{ r: 6, fill: "#f59e0b" }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Sentimiento por Fuente */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-800">
            Sentimiento por Fuente
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {sentimentSources.map((source, index) => (
              <div key={index} className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    <div 
                      className="w-3 h-3 rounded-full" 
                      style={{ backgroundColor: source.color }}
                    />
                    <span className="text-gray-800 font-medium">{source.name}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    {getSentimentIcon(source.value)}
                    <span className={`text-sm font-medium ${
                      source.change >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {source.change >= 0 ? '+' : ''}{source.change.toFixed(1)}%
                    </span>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-2xl font-bold text-gray-900">
                      {source.value}
                    </span>
                    <span className="text-sm text-gray-500">
                      {formatNumber(source.posts)} posts
                    </span>
                  </div>
                  
                  <Progress 
                    value={source.value} 
                    className="h-2"
                    style={{ 
                      '--progress-background': source.color 
                    }}
                  />
                  
                  <div className="flex justify-between text-xs text-gray-500">
                    <span>Bearish</span>
                    <span>Neutral</span>
                    <span>Bullish</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Resumen de Sentimiento */}
        <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-1">
                Sentimiento General
              </h3>
              <p className="text-sm text-gray-500">
                Basado en múltiples fuentes de datos
              </p>
            </div>
            <div className="text-right">
              <div className="flex items-center space-x-2 mb-1">
                <TrendingUp className="h-5 w-5 text-green-600" />
                <Badge variant="secondary" className="bg-green-100 text-green-700 border-green-200">
                  Bullish
                </Badge>
              </div>
              <div className="text-sm text-gray-500">
                Confianza: 78%
              </div>
            </div>
          </div>
          
          <div className="mt-4 grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-lg font-semibold text-green-600">
                {sentimentSources.filter(s => s.value > 60).length}
              </div>
              <div className="text-xs text-gray-500">Fuentes Bullish</div>
            </div>
            <div>
              <div className="text-lg font-semibold text-amber-600">
                {sentimentSources.filter(s => s.value >= 40 && s.value <= 60).length}
              </div>
              <div className="text-xs text-gray-500">Fuentes Neutrales</div>
            </div>
            <div>
              <div className="text-lg font-semibold text-red-600">
                {sentimentSources.filter(s => s.value < 40).length}
              </div>
              <div className="text-xs text-gray-500">Fuentes Bearish</div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default SentimentAnalysis;

