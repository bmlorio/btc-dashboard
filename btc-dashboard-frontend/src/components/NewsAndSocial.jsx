import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  MessageCircle, 
  ExternalLink, 
  TrendingUp, 
  Clock, 
  Heart,
  Share,
  Eye,
  Globe,
  Twitter,
  Hash
} from 'lucide-react';

const NewsAndSocial = () => {
  const [newsData] = useState([
    {
      id: 1,
      title: 'Bitcoin alcanza nuevo máximo mensual tras adopción institucional',
      summary: 'El precio de Bitcoin ha superado los $68,000 después de que varias instituciones anunciaran nuevas inversiones en criptomonedas.',
      source: 'CoinDesk',
      timestamp: new Date(Date.now() - 15 * 60 * 1000),
      sentiment: 'positive',
      category: 'market'
    },
    {
      id: 2,
      title: 'Reguladores europeos proponen nuevas reglas para exchanges',
      summary: 'La Unión Europea está considerando implementar regulaciones más estrictas para los exchanges de criptomonedas.',
      source: 'Reuters',
      timestamp: new Date(Date.now() - 45 * 60 * 1000),
      sentiment: 'negative',
      category: 'regulation'
    },
    {
      id: 3,
      title: 'Análisis técnico: Bitcoin muestra señales de continuación alcista',
      summary: 'Los indicadores técnicos sugieren que Bitcoin podría continuar su tendencia alcista en las próximas semanas.',
      source: 'TradingView',
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000),
      sentiment: 'positive',
      category: 'analysis'
    }
  ]);

  const [socialData] = useState([
    {
      id: 1,
      platform: 'reddit',
      title: 'Bitcoin está rompiendo resistencia clave en $68K',
      author: 'CryptoTrader2024',
      subreddit: 'r/Bitcoin',
      score: 1250,
      comments: 89,
      timestamp: new Date(Date.now() - 20 * 60 * 1000),
      sentiment: 'positive'
    },
    {
      id: 2,
      platform: 'twitter',
      title: 'El volumen de Bitcoin está aumentando significativamente. Esto podría ser el inicio de la próxima leg up. #Bitcoin #BTC',
      author: '@BitcoinAnalyst',
      followers: 125000,
      likes: 450,
      retweets: 89,
      timestamp: new Date(Date.now() - 35 * 60 * 1000),
      sentiment: 'positive'
    },
    {
      id: 3,
      platform: 'reddit',
      title: '¿Alguien más está preocupado por la regulación en Europa?',
      author: 'EuroHodler',
      subreddit: 'r/CryptoCurrency',
      score: 567,
      comments: 123,
      timestamp: new Date(Date.now() - 1 * 60 * 60 * 1000),
      sentiment: 'negative'
    }
  ]);

  const [trendingTopics] = useState([
    { tag: '#Bitcoin', mentions: 15420, change: +12.5 },
    { tag: '#BTC', mentions: 8930, change: +8.2 },
    { tag: '#Crypto', mentions: 6750, change: -2.1 },
    { tag: '#Blockchain', mentions: 4320, change: +5.7 },
    { tag: '#DeFi', mentions: 3890, change: +15.3 }
  ]);

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'positive': return 'text-green-600 bg-green-100 border-green-200';
      case 'negative': return 'text-red-600 bg-red-100 border-red-200';
      case 'neutral': return 'text-amber-600 bg-amber-100 border-amber-200';
      default: return 'text-gray-500 bg-gray-100 border-gray-200';
    }
  };

  const getCategoryColor = (category) => {
    switch (category) {
      case 'market': return 'text-blue-600 bg-blue-100 border-blue-200';
      case 'regulation': return 'text-orange-600 bg-orange-100 border-orange-200';
      case 'analysis': return 'text-purple-600 bg-purple-100 border-purple-200';
      case 'technology': return 'text-green-600 bg-green-100 border-green-200';
      default: return 'text-gray-500 bg-gray-100 border-gray-200';
    }
  };

  const getPlatformIcon = (platform) => {
    switch (platform) {
      case 'twitter': return <Twitter className="h-4 w-4 text-blue-600" />;
      case 'reddit': return <MessageCircle className="h-4 w-4 text-orange-600" />;
      default: return <Globe className="h-4 w-4 text-gray-400" />;
    }
  };

  const formatTime = (timestamp) => {
    const now = new Date();
    const diff = Math.floor((now - timestamp) / (1000 * 60));
    if (diff < 1) return 'Ahora';
    if (diff < 60) return `${diff}m`;
    if (diff < 1440) return `${Math.floor(diff / 60)}h`;
    return `${Math.floor(diff / 1440)}d`;
  };

  const formatNumber = (value) => {
    return new Intl.NumberFormat('es-ES', {
      notation: 'compact',
      maximumFractionDigits: 1
    }).format(value);
  };

  return (
    <Card className="bg-white border border-gray-200 shadow-sm">
      <CardHeader>
        <CardTitle className="text-gray-800 flex items-center space-x-2">
          <Globe className="h-5 w-5 text-blue-600" />
          <span>Noticias y Redes Sociales</span>
        </CardTitle>
        <CardDescription className="text-gray-500">
          últimas noticias y tendencias en redes sociales
        </CardDescription>
      </CardHeader>

      <CardContent>
        <Tabs defaultValue="news" className="space-y-4">
          <TabsList className="grid w-full grid-cols-3 bg-white border border-gray-200 rounded-md">
            <TabsTrigger value="news" className="text-gray-700 data-[state=active]:bg-blue-600 data-[state=active]:text-white">Noticias</TabsTrigger>
            <TabsTrigger value="social" className="text-gray-700 data-[state=active]:bg-blue-600 data-[state=active]:text-white">Social</TabsTrigger>
            <TabsTrigger value="trending" className="text-gray-700 data-[state=active]:bg-blue-600 data-[state=active]:text-white">Trending</TabsTrigger>
          </TabsList>

          <TabsContent value="news" className="space-y-4">
            {newsData.map((news) => (
              <div key={news.id} className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <Badge className={getCategoryColor(news.category)}>{news.category}</Badge>
                    <Badge className={getSentimentColor(news.sentiment)}>{news.sentiment}</Badge>
                  </div>
                  <div className="flex items-center space-x-2 text-sm text-gray-400">
                    <Clock className="h-4 w-4" />
                    <span>{formatTime(news.timestamp)}</span>
                  </div>
                </div>

                <h3 className="text-gray-800 font-semibold mb-2 line-clamp-2">{news.title}</h3>
                <p className="text-gray-500 text-sm mb-3 line-clamp-2">{news.summary}</p>

                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Globe className="h-4 w-4 text-gray-400" />
                    <span className="text-sm text-gray-500">{news.source}</span>
                  </div>
                  <Button variant="ghost" size="sm" className="text-blue-400 hover:text-blue-300">
                    <ExternalLink className="h-4 w-4 mr-1" />Leer más
                  </Button>
                </div>
              </div>
            ))}
          </TabsContent>

          <TabsContent value="social" className="space-y-4">
            {socialData.map((post) => (
              <div key={post.id} className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    {getPlatformIcon(post.platform)}
                    <span className="text-sm font-medium text-gray-800">{post.author}</span>
                    {post.subreddit && <span className="text-sm text-gray-500">{post.subreddit}</span>}
                    {post.followers && <span className="text-sm text-gray-500">{formatNumber(post.followers)} seguidores</span>}
                  </div>
                  <div className="flex items-center space-x-2 text-sm text-gray-400">
                    <Clock className="h-4 w-4" />
                    <span>{formatTime(post.timestamp)}</span>
                  </div>
                </div>

                <p className="text-gray-500 text-sm mb-3">{post.title}</p>

                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    {post.platform === 'reddit' && (
                      <>
                        <div className="flex items-center space-x-1">
                          <TrendingUp className="h-4 w-4 text-orange-600" />
                          <span className="text-sm text-gray-400">{formatNumber(post.score)}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <MessageCircle className="h-4 w-4 text-blue-600" />
                          <span className="text-sm text-gray-400">{post.comments}</span>
                        </div>
                      </>
                    )}
                    {post.platform === 'twitter' && (
                      <>
                        <div className="flex items-center space-x-1">
                          <Heart className="h-4 w-4 text-red-600" />
                          <span className="text-sm text-gray-400">{formatNumber(post.likes)}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <Share className="h-4 w-4 text-green-600" />
                          <span className="text-sm text-gray-400">{post.retweets}</span>
                        </div>
                      </>
                    )}
                  </div>
                  <Badge className={getSentimentColor(post.sentiment)}>{post.sentiment}</Badge>
                </div>
              </div>
            ))}
          </TabsContent>

          <TabsContent value="trending" className="space-y-4">
            <div className="grid grid-cols-1 gap-3">
              {trendingTopics.map((topic, index) => (
                <div key={index} className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="flex items-center space-x-2">
                        <Hash className="h-4 w-4 text-blue-600" />
                        <span className="text-gray-800 font-medium">{topic.tag}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Eye className="h-4 w-4 text-gray-400" />
                        <span className="text-sm text-gray-400">{formatNumber(topic.mentions)} menciones</span>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      {topic.change >= 0 ? (
                        <TrendingUp className="h-4 w-4 text-green-600" />
                      ) : (
                        <TrendingUp className="h-4 w-4 text-red-600 rotate-180" />
                      )}
                      <span className={`text-sm font-medium ${topic.change >= 0 ? 'text-green-600' : 'text-red-600'}`}>{topic.change >= 0 ? '+' : ''}{topic.change.toFixed(1)}%</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
              <h3 className="text-gray-800 font-semibold mb-3">Resumen de Tendencias</h3>
              <div className="grid grid-cols-2 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-green-600">{trendingTopics.filter(t => t.change > 0).length}</div>
                  <div className="text-sm text-gray-500">Tendencias al alza</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-red-600">{trendingTopics.filter(t => t.change < 0).length}</div>
                  <div className="text-sm text-gray-500">Tendencias a la baja</div>
                </div>
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
};

export default NewsAndSocial;

