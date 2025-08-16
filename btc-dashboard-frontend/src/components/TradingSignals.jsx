import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  TrendingUp, 
  TrendingDown, 
  Target, 
  AlertTriangle, 
  CheckCircle, 
  XCircle,
  Clock,
  Zap,
  BarChart3,
  Activity
} from 'lucide-react';

const TradingSignals = () => {
  const [signals, setSignals] = useState([
    {
      id: 1,
      type: 'BUY',
      strength: 'STRONG',
      price: 67850,
      timestamp: new Date(Date.now() - 5 * 60 * 1000),
      indicator: 'RSI Oversold + Volume Spike',
      target: 70500,
      stopLoss: 66200,
      confidence: 85,
      status: 'ACTIVE',
      pnl: null
    },
    {
      id: 2,
      type: 'SELL',
      strength: 'MEDIUM',
      price: 68200,
      timestamp: new Date(Date.now() - 25 * 60 * 1000),
      indicator: 'Resistance Level + Bearish Divergence',
      target: 66800,
      stopLoss: 69000,
      confidence: 72,
      status: 'CLOSED',
      pnl: 1400
    },
    {
      id: 3,
      type: 'BUY',
      strength: 'WEAK',
      price: 67200,
      timestamp: new Date(Date.now() - 45 * 60 * 1000),
      indicator: 'Support Bounce',
      target: 68500,
      stopLoss: 66500,
      confidence: 58,
      status: 'CLOSED',
      pnl: -700
    },
    {
      id: 4,
      type: 'HOLD',
      strength: 'MEDIUM',
      price: 67850,
      timestamp: new Date(Date.now() - 2 * 60 * 1000),
      indicator: 'Consolidation Pattern',
      target: null,
      stopLoss: null,
      confidence: 65,
      status: 'ACTIVE',
      pnl: null
    }
  ]);

  const [technicalIndicators, setTechnicalIndicators] = useState({
    rsi: { value: 32, signal: 'OVERSOLD', strength: 'STRONG' },
    macd: { value: 0.15, signal: 'BULLISH', strength: 'MEDIUM' },
    bb: { value: 'LOWER', signal: 'OVERSOLD', strength: 'MEDIUM' },
    ema: { value: 'ABOVE', signal: 'BULLISH', strength: 'WEAK' },
    volume: { value: 'HIGH', signal: 'BULLISH', strength: 'STRONG' },
    support: { value: 67200, signal: 'HOLDING', strength: 'STRONG' },
    resistance: { value: 69500, signal: 'STRONG', strength: 'STRONG' }
  });

  const getSignalColor = (type) => {
    switch (type) {
      case 'BUY': return 'text-green-500 bg-green-500/20 border-green-500/30';
      case 'SELL': return 'text-red-500 bg-red-500/20 border-red-500/30';
      case 'HOLD': return 'text-yellow-500 bg-yellow-500/20 border-yellow-500/30';
      default: return 'text-gray-500 bg-gray-500/20 border-gray-500/30';
    }
  };

  const getStrengthColor = (strength) => {
    switch (strength) {
      case 'STRONG': return 'text-green-400';
      case 'MEDIUM': return 'text-yellow-400';
      case 'WEAK': return 'text-orange-400';
      default: return 'text-gray-400';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'ACTIVE': return <Clock className="h-4 w-4 text-blue-500" />;
      case 'CLOSED': return <CheckCircle className="h-4 w-4 text-gray-500" />;
      default: return <XCircle className="h-4 w-4 text-red-500" />;
    }
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(price);
  };

  const formatTime = (timestamp) => {
    const now = new Date();
    const diff = Math.floor((now - timestamp) / (1000 * 60));
    
    if (diff < 1) return 'Ahora';
    if (diff < 60) return `${diff}m`;
    if (diff < 1440) return `${Math.floor(diff / 60)}h`;
    return `${Math.floor(diff / 1440)}d`;
  };

  const getIndicatorIcon = (indicator) => {
    if (indicator.toLowerCase().includes('rsi')) return <Activity className="h-4 w-4" />;
    if (indicator.toLowerCase().includes('volume')) return <BarChart3 className="h-4 w-4" />;
    if (indicator.toLowerCase().includes('resistance') || indicator.toLowerCase().includes('support')) return <Target className="h-4 w-4" />;
    return <Zap className="h-4 w-4" />;
  };

  const activeSignals = signals.filter(s => s.status === 'ACTIVE');
  const totalPnL = signals.filter(s => s.pnl !== null).reduce((sum, s) => sum + s.pnl, 0);
  const winRate = signals.filter(s => s.pnl !== null).length > 0 
    ? (signals.filter(s => s.pnl > 0).length / signals.filter(s => s.pnl !== null).length) * 100 
    : 0;

  return (
    <div className="space-y-6">
      {/* Resumen de Señales */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-white border border-gray-200 shadow-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-700">
              Señales Activas
            </CardTitle>
            <Zap className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">
              {activeSignals.length}
            </div>
            <p className="text-xs text-gray-500 mt-1">
              En seguimiento
            </p>
          </CardContent>
        </Card>

        <Card className="bg-white border border-gray-200 shadow-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-700">
              P&L Total
            </CardTitle>
            {totalPnL >= 0 ? (
              <TrendingUp className="h-4 w-4 text-green-600" />
            ) : (
              <TrendingDown className="h-4 w-4 text-red-600" />
            )}
          </CardHeader>
          <CardContent>
            <div className={`text-2xl font-bold ${totalPnL >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {formatPrice(totalPnL)}
            </div>
            <p className="text-xs text-gray-500 mt-1">
              últimas 24h
            </p>
          </CardContent>
        </Card>

        <Card className="bg-white border border-gray-200 shadow-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-700">
              Tasa de Acierto
            </CardTitle>
            <Target className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">
              {winRate.toFixed(0)}%
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Señales cerradas
            </p>
          </CardContent>
        </Card>

        <Card className="bg-white border border-gray-200 shadow-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-700">
              Confianza Promedio
            </CardTitle>
            <CheckCircle className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">
              {Math.round(activeSignals.reduce((sum, s) => sum + s.confidence, 0) / activeSignals.length || 0)}%
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Señales activas
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Indicadores Técnicos */}
      <Card className="bg-white border border-gray-200 shadow-sm">
        <CardHeader>
          <CardTitle className="text-gray-800 flex items-center space-x-2">
            <Activity className="h-5 w-5 text-purple-600" />
            <span>Indicadores Técnicos</span>
          </CardTitle>
          <CardDescription className="text-gray-500">
            Estado actual de los principales indicadores
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">RSI (14)</span>
                <Badge className={getSignalColor('BUY')}>
                  {technicalIndicators.rsi.signal}
                </Badge>
              </div>
              <div className="text-xl font-bold text-gray-900">
                {technicalIndicators.rsi.value}
              </div>
              <div className={`text-sm ${getStrengthColor(technicalIndicators.rsi.strength)}`}>
                {technicalIndicators.rsi.strength}
              </div>
            </div>

            <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">MACD</span>
                <Badge className={getSignalColor('BUY')}>
                  {technicalIndicators.macd.signal}
                </Badge>
              </div>
              <div className="text-xl font-bold text-gray-900">
                {technicalIndicators.macd.value}
              </div>
              <div className={`text-sm ${getStrengthColor(technicalIndicators.macd.strength)}`}>
                {technicalIndicators.macd.strength}
              </div>
            </div>

            <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">Bollinger</span>
                <Badge className={getSignalColor('BUY')}>
                  {technicalIndicators.bb.signal}
                </Badge>
              </div>
              <div className="text-xl font-bold text-gray-900">
                {technicalIndicators.bb.value}
              </div>
              <div className={`text-sm ${getStrengthColor(technicalIndicators.bb.strength)}`}>
                {technicalIndicators.bb.strength}
              </div>
            </div>

            <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">Volumen</span>
                <Badge className={getSignalColor('BUY')}>
                  {technicalIndicators.volume.signal}
                </Badge>
              </div>
              <div className="text-xl font-bold text-gray-900">
                {technicalIndicators.volume.value}
              </div>
              <div className={`text-sm ${getStrengthColor(technicalIndicators.volume.strength)}`}>
                {technicalIndicators.volume.strength}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Lista de Señales */}
      <Card className="bg-white border border-gray-200 shadow-sm">
        <CardHeader>
          <CardTitle className="text-gray-800 flex items-center space-x-2">
            <Target className="h-5 w-5 text-orange-600" />
            <span>Señales de Trading</span>
          </CardTitle>
          <CardDescription className="text-gray-500">
            Historial y señales activas basadas en análisis técnico
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {signals.map((signal) => (
              <div key={signal.id} className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    <Badge className={getSignalColor(signal.type)}>
                      {signal.type}
                    </Badge>
                    <Badge variant="outline" className={`border-gray-200 ${getStrengthColor(signal.strength)}`}>
                      {signal.strength}
                    </Badge>
                    <div className="flex items-center space-x-1">
                      {getStatusIcon(signal.status)}
                      <span className="text-sm text-gray-500">{signal.status}</span>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-gray-500">
                      {formatTime(signal.timestamp)}
                    </div>
                    <div className="text-sm font-medium text-gray-800">
                      Confianza: {signal.confidence}%
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-3">
                  <div>
                    <div className="text-xs text-gray-500">Precio de Entrada</div>
                    <div className="text-sm font-medium text-gray-800">
                      {formatPrice(signal.price)}
                    </div>
                  </div>
                  {signal.target && (
                    <div>
                      <div className="text-xs text-gray-500">Objetivo</div>
                      <div className="text-sm font-medium text-green-600">
                        {formatPrice(signal.target)}
                      </div>
                    </div>
                  )}
                  {signal.stopLoss && (
                    <div>
                      <div className="text-xs text-gray-500">Stop Loss</div>
                      <div className="text-sm font-medium text-red-600">
                        {formatPrice(signal.stopLoss)}
                      </div>
                    </div>
                  )}
                  {signal.pnl !== null && (
                    <div>
                      <div className="text-xs text-gray-500">P&L</div>
                      <div className={`text-sm font-medium ${signal.pnl >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {formatPrice(signal.pnl)}
                      </div>
                    </div>
                  )}
                </div>

                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  {getIndicatorIcon(signal.indicator)}
                  <span>{signal.indicator}</span>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Alerta de Señal Fuerte */}
      {activeSignals.some(s => s.strength === 'STRONG') && (
        <Alert className="bg-white border border-gray-200 text-gray-800 transform transition-transform duration-200 hover:-translate-y-0.5 shadow-sm">
          <AlertTriangle className="h-4 w-4 text-orange-500" />
          <AlertDescription className="text-gray-700">
            <strong>Señal Fuerte Detectada:</strong> Se ha identificado una oportunidad de trading con alta confianza. 
            Revisa los niveles de entrada, objetivo y stop loss antes de operar.
          </AlertDescription>
        </Alert>
      )}
    </div>
  );
};

export default TradingSignals;

