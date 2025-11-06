import React from 'react';
import {
  Box,
  Text,
  VStack,
  HStack,
  Link,
  Icon,
  Badge,
  Divider,
} from '@chakra-ui/react';
import { ExternalLinkIcon } from '@chakra-ui/icons';

const NewsArticles = ({ articles }) => {
  if (!articles || articles.length === 0) {
    return (
      <Box
        p={6}
        borderWidth="1px"
        borderRadius="lg"
        bg="gray.800"
        borderColor="gray.700"
        shadow="lg"
      >
        <VStack align="stretch" spacing={3}>
          <HStack>
            <Icon as={ExternalLinkIcon} color="blue.400" boxSize={5} />
            <Text fontSize="lg" fontWeight="bold" color="white">
              News API Articles
            </Text>
          </HStack>
          <Text color="gray.400" fontSize="sm">
            No recent news articles found related to this IP infrastructure.
          </Text>
        </VStack>
      </Box>
    );
  }

  return (
    <Box
      p={6}
      borderWidth="1px"
      borderRadius="lg"
      bg="gray.800"
      borderColor="blue.500"
      shadow="lg"
    >
      <VStack align="stretch" spacing={4}>
        <HStack justify="space-between">
          <HStack>
            <Icon as={ExternalLinkIcon} color="blue.400" boxSize={5} />
            <Text fontSize="lg" fontWeight="bold" color="white">
              Related Security News
            </Text>
          </HStack>
          <Badge colorScheme="blue" fontSize="xs" px={2} py={1}>
            {articles.length} ARTICLES
          </Badge>
        </HStack>

        <Divider borderColor="gray.700" />

        <VStack align="stretch" spacing={3}>
          {articles.map((article, index) => (
            <Box
              key={index}
              p={4}
              bg="gray.900"
              borderRadius="md"
              borderLeft="4px"
              borderColor="blue.400"
              _hover={{
                bg: 'gray.750',
                transform: 'translateX(4px)',
                transition: 'all 0.2s'
              }}
            >
              <VStack align="stretch" spacing={2}>
                <HStack justify="space-between" align="start">
                  <Text color="blue.300" fontSize="sm" fontWeight="bold">
                    {article.source}
                  </Text>
                  <Text color="gray.500" fontSize="xs">
                    {new Date(article.publishedAt).toLocaleDateString()}
                  </Text>
                </HStack>
                
                <Link 
                  href={article.url} 
                  isExternal
                  _hover={{ textDecoration: 'none' }}
                >
                  <Text 
                    color="white" 
                    fontSize="md" 
                    fontWeight="semibold"
                    _hover={{ color: 'blue.300' }}
                  >
                    {article.title}
                  </Text>
                </Link>
                
                {article.description && (
                  <Text color="gray.400" fontSize="sm" noOfLines={2}>
                    {article.description}
                  </Text>
                )}
                
                <Link 
                  href={article.url} 
                  isExternal
                  fontSize="xs"
                  color="blue.400"
                  _hover={{ color: 'blue.300' }}
                >
                  Read full article <ExternalLinkIcon mx={1} />
                </Link>
              </VStack>
            </Box>
          ))}
        </VStack>

        <Box
          p={3}
          bg="blue.900"
          borderRadius="md"
          borderLeft="3px"
          borderColor="blue.500"
        >
          <Text fontSize="xs" color="blue.200" fontWeight="medium">
            ℹ️ Articles sourced from News API based on infrastructure patterns and cybersecurity keywords.
          </Text>
        </Box>
      </VStack>
    </Box>
  );
};

export default NewsArticles;
