import React, { useMemo, useState } from 'react';
import {
  Box,
  Text,
  Input,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  HStack,
  Button,
  Badge,
  VStack,
  Link,
} from '@chakra-ui/react';

const PAGE_SIZE = 10;

const formatDate = (ts) => {
  if (!ts) return '—';
  try {
    return new Date(ts * 1000).toLocaleString();
  } catch {
    return '—';
  }
};

const statBadge = (value, type) => {
  const color = type === 'malicious' ? 'red' : type === 'suspicious' ? 'orange' : type === 'harmless' ? 'green' : 'gray';
  return (
    <Badge colorScheme={color} variant="subtle" px={2} py={1} borderRadius="md">
      {Number.isFinite(value) ? value : 0}
    </Badge>
  );
};

const vtUrlLink = (url) => `https://www.virustotal.com/gui/search/${encodeURIComponent(url || '')}`;

const VirusTotalURLTable = ({ urls = [] }) => {
  const [query, setQuery] = useState('');
  const [page, setPage] = useState(1);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return urls;
    return urls.filter((u) => (u.url || '').toLowerCase().includes(q));
  }, [urls, query]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const currentPage = Math.min(page, totalPages);
  const start = (currentPage - 1) * PAGE_SIZE;
  const pageItems = filtered.slice(start, start + PAGE_SIZE);

  return (
    <Box p={6} borderWidth="1px" borderRadius="lg" bg="gray.800" borderColor="gray.700" shadow="lg">
      <VStack align="stretch" spacing={4}>
        <HStack justify="space-between">
          <Text fontSize="lg" fontWeight="bold" color="white">
            VirusTotal Related URLs
          </Text>
          <Input
            placeholder="Search URL"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setPage(1);
            }}
            maxW="300px"
            bg="gray.900"
            borderColor="gray.600"
            color="white"
            _hover={{ borderColor: 'gray.500' }}
          />
        </HStack>

        <Table size="sm" variant="simple">
          <Thead>
            <Tr>
              <Th color="gray.300" borderColor="gray.700">URL</Th>
              <Th color="gray.300" borderColor="gray.700">Malicious</Th>
              <Th color="gray.300" borderColor="gray.700">Suspicious</Th>
              <Th color="gray.300" borderColor="gray.700">Harmless</Th>
              <Th color="gray.300" borderColor="gray.700">Undetected</Th>
              <Th color="gray.300" borderColor="gray.700">Last Seen</Th>
            </Tr>
          </Thead>
          <Tbody>
            {pageItems.map((item, idx) => {
              const stats = item.last_analysis_stats || {};
              return (
                <Tr key={`${item.url}-${idx}`}>
                  <Td borderColor="gray.700">
                    <Link href={vtUrlLink(item.url)} isExternal color="blue.400" _hover={{ color: 'blue.300' }}>
                      {item.url || '—'}
                    </Link>
                  </Td>
                  <Td borderColor="gray.700">{statBadge(stats.malicious, 'malicious')}</Td>
                  <Td borderColor="gray.700">{statBadge(stats.suspicious, 'suspicious')}</Td>
                  <Td borderColor="gray.700">{statBadge(stats.harmless, 'harmless')}</Td>
                  <Td borderColor="gray.700">{statBadge(stats.undetected, 'undetected')}</Td>
                  <Td borderColor="gray.700" color="gray.300">{formatDate(item.last_submission_date)}</Td>
                </Tr>
              );
            })}
            {pageItems.length === 0 && (
              <Tr>
                <Td colSpan={6} textAlign="center" color="gray.400" borderColor="gray.700">
                  No URLs found
                </Td>
              </Tr>
            )}
          </Tbody>
        </Table>

        <HStack justify="space-between">
          <Text fontSize="sm" color="gray.400">
            {filtered.length} results • Page {currentPage} of {totalPages}
          </Text>
          <HStack>
            <Button size="sm" onClick={() => setPage((p) => Math.max(1, p - 1))} isDisabled={currentPage <= 1}>
              Previous
            </Button>
            <Button size="sm" onClick={() => setPage((p) => Math.min(totalPages, p + 1))} isDisabled={currentPage >= totalPages}>
              Next
            </Button>
          </HStack>
        </HStack>
      </VStack>
    </Box>
  );
};

export default VirusTotalURLTable;
